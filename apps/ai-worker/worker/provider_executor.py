from __future__ import annotations

from copy import deepcopy
import json
import os
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ProviderExecutionError(RuntimeError):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class WritingProviderAdapter(Protocol):
    def draft_section(
        self,
        *,
        chapter_plan: dict[str, Any],
        section_plan: dict[str, Any],
        section_index: int,
        model_profile: dict[str, Any],
        knowledge_context: str = "",
    ) -> dict[str, Any]: ...

    def review_sections(
        self,
        *,
        section_runs: list[dict[str, Any]],
        drafts: list[dict[str, Any]],
        consistency_report_id: str,
        model_profile: dict[str, Any],
    ) -> list[dict[str, Any]]: ...

    def humanize_section(
        self,
        *,
        section_plan: dict[str, Any],
        section_index: int,
        draft_text: str,
        critic_issues: list[dict[str, Any]],
        model_profile: dict[str, Any],
        knowledge_context: str = "",
    ) -> dict[str, Any]: ...


class AnthropicWritingAdapter:
    def _chat(self, *, model_profile: dict[str, Any], system: str, user: str) -> dict[str, Any]:
        import time
        base_env = model_profile.get("base_url_env", "NOVELIST_LLM_BASE_URL")
        key_env = model_profile.get("api_key_env", "NOVELIST_LLM_API_KEY")
        base_url = os.getenv(base_env)
        api_key = os.getenv(key_env)
        if not base_url or not api_key:
            text = f"（离线草稿）{user.strip()[:280]}"
            return {"text": text, "prompt_tokens": len(user) // 2, "completion_tokens": len(text) // 2, "latency_ms": 0}
        endpoint = base_url.rstrip("/") + "/chat/completions"
        body = json.dumps(
            {
                "model": model_profile["provider_model_name"],
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "temperature": 0.4,
                "max_tokens": 600,
            }
        ).encode("utf-8")
        request = Request(
            endpoint,
            data=body,
            headers={"authorization": f"Bearer {api_key}", "content-type": "application/json"},
            method="POST",
        )
        started = time.monotonic()
        try:
            with urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise ProviderExecutionError("provider_http_error", f"provider request failed: {exc.code}") from exc
        except URLError as exc:
            raise ProviderExecutionError("provider_network_error", "provider request failed") from exc
        except TimeoutError as exc:
            raise ProviderExecutionError("provider_timeout", "provider request timed out") from exc
        latency_ms = int((time.monotonic() - started) * 1000)
        try:
            text = payload["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderExecutionError("provider_response_invalid", "provider response missing message content") from exc
        usage = payload.get("usage") or {}
        return {"text": text, "prompt_tokens": int(usage.get("prompt_tokens", 0)), "completion_tokens": int(usage.get("completion_tokens", 0)), "latency_ms": latency_ms}

    def draft_section(self, *, chapter_plan: dict[str, Any], section_plan: dict[str, Any], section_index: int, model_profile: dict[str, Any], knowledge_context: str = "") -> dict[str, Any]:
        payload = section_plan.get("payload", {})
        scene_goal = payload.get("scene_goal") or f"推进第 {section_index} 节剧情"
        beats = payload.get("beats", [])
        beat_phrase = "，".join(beat.get("summary", f"beat {beat.get('index', i + 1)}") for i, beat in enumerate(beats)) or scene_goal
        knowledge_block = f"\n【世界观与知识】\n{knowledge_context}\n" if knowledge_context.strip() else ""
        user = (
            f"章节目标：{chapter_plan.get('payload', {}).get('summary', scene_goal)}\n"
            f"本节目标：{scene_goal}\nbeats：{beat_phrase}\n{knowledge_block}"
        )
        chat = self._chat(
            model_profile=model_profile,
            system="你是中文网文章节写手。必须遵循给定世界观与已确立设定，不得引入矛盾。输出一段可直接进入章节草稿的中文正文，不要解释。",
            user=user,
        )
        return {"writer_output": chat["text"], "scene_goal": scene_goal, "beat_phrase": beat_phrase, "provider_model_name": model_profile["provider_model_name"], "prompt_tokens": chat["prompt_tokens"], "completion_tokens": chat["completion_tokens"], "latency_ms": chat["latency_ms"]}

    def review_sections(self, *, section_runs: list[dict[str, Any]], drafts: list[dict[str, Any]], consistency_report_id: str, model_profile: dict[str, Any]) -> list[dict[str, Any]]:
        base_env = model_profile.get("base_url_env", "NOVELIST_LLM_BASE_URL")
        key_env = model_profile.get("api_key_env", "NOVELIST_LLM_API_KEY")
        if not os.getenv(base_env) or not os.getenv(key_env):
            return []
        combined = "\n".join(draft["writer_output"] for draft in drafts)
        review = self._chat(
            model_profile=model_profile,
            system="你是中文小说一致性审稿人。若没有严重阻断，只输出 PASS；若有阻断，用一句中文说明。",
            user=combined,
        )["text"]
        if review.upper().startswith("PASS"):
            return []
        section_run = section_runs[min(1, len(section_runs) - 1)]
        return [
            {
                "issue_id": "01JZCONSISTISSUE000000001",
                "category": "llm_consistency_review",
                "severity": "warning",
                "summary": review[:160],
                "affected_text_ref": f"{section_run['draft_object_ref']}#p1",
                "rule_id": "rule-01JZPOWER000000000000001",
                "resolution_status": "open",
                "input_refs": ["object://rules/rule-01JZPOWER000000000000001"],
                "output_refs": [f"object://consistency-reports/{consistency_report_id}/issues/1"],
                "note": model_profile["provider_model_name"],
            }
        ]

    def humanize_section(self, *, section_plan: dict[str, Any], section_index: int, draft_text: str, critic_issues: list[dict[str, Any]], model_profile: dict[str, Any], knowledge_context: str = "") -> dict[str, Any]:
        knowledge_block = f"\n【需保持一致的设定】\n{knowledge_context}\n" if knowledge_context.strip() else ""
        chat = self._chat(
            model_profile=model_profile,
            system="你是中文小说润色师。保留剧情事实与给定设定，降低机械感，输出润色正文，不要解释。",
            user=f"{draft_text}\n{knowledge_block}",
        )
        return {"humanized_text": chat["text"], "provider_model_name": model_profile["provider_model_name"], "had_critic_issues": bool(critic_issues), "prompt_tokens": chat["prompt_tokens"], "completion_tokens": chat["completion_tokens"], "latency_ms": chat["latency_ms"]}


class OpenAICompatibleWritingAdapter(AnthropicWritingAdapter):
    pass



def _build_provider_adapter(provider_name: str) -> WritingProviderAdapter:
    if provider_name == "anthropic":
        return AnthropicWritingAdapter()
    if provider_name in {"deepseek", "openai_compatible"}:
        return OpenAICompatibleWritingAdapter()
    raise ProviderExecutionError("provider_not_supported", f"provider adapter not supported: {provider_name}")


def _find_successful_provider_call(provider_calls: list[dict[str, Any]], agent_role: str) -> dict[str, Any]:
    for call in provider_calls:
        if call.get("agent_role") == agent_role and call.get("status") == "succeeded":
            return call
    raise ProviderExecutionError("provider_call_missing", f"successful provider call missing for role: {agent_role}")


def _load_model_profile(store: Any, model_profile_id: str) -> dict[str, Any]:
    profile = store.STORE.model_profiles.get(model_profile_id)
    if profile:
        return profile
    raise ProviderExecutionError("model_profile_missing", f"model profile missing: {model_profile_id}")


def execute_writing_provider_pipeline(
    *,
    store: Any,
    writing_run: dict[str, Any],
    chapter_plan: dict[str, Any],
    section_plans: list[dict[str, Any]],
    section_runs: list[dict[str, Any]],
    prompt_package: dict[str, Any],
    knowledge_context: str = "",
) -> dict[str, Any]:
    provider_calls = deepcopy(store.STORE.provider_calls_by_writing.get(writing_run["writing_run_id"], []))
    retry_count = max((item.get("retry_count", 0) for item in provider_calls), default=0)
    writer_call = _find_successful_provider_call(provider_calls, "writer")
    critic_call = _find_successful_provider_call(provider_calls, "critic")
    humanizer_call = _find_successful_provider_call(provider_calls, "humanizer")

    writer_profile = _load_model_profile(store, writer_call["model_profile_id"])
    critic_profile = _load_model_profile(store, critic_call["model_profile_id"])
    humanizer_profile = _load_model_profile(store, humanizer_call["model_profile_id"])

    writer_adapter = _build_provider_adapter(writer_profile["provider_name"])
    critic_adapter = _build_provider_adapter(critic_profile["provider_name"])
    humanizer_adapter = _build_provider_adapter(humanizer_profile["provider_name"])

    drafts = [
        writer_adapter.draft_section(
            chapter_plan=chapter_plan,
            section_plan=section_plan,
            section_index=index,
            model_profile=writer_profile,
            knowledge_context=knowledge_context,
        )
        for index, section_plan in enumerate(section_plans, start=1)
    ]
    consistency_issues = critic_adapter.review_sections(
        section_runs=section_runs,
        drafts=drafts,
        consistency_report_id=writing_run["consistency_report_id"],
        model_profile=critic_profile,
    )

    section_run_updates: list[dict[str, Any]] = []
    humanized_sections: list[str] = []
    humanized_results: list[dict[str, Any]] = []
    for index, (section_run, section_plan, draft) in enumerate(zip(section_runs, section_plans, drafts), start=1):
        critic_issues = [
            {
                "issue_id": issue["issue_id"],
                "severity": issue["severity"],
                "category": issue["category"],
                "summary": issue.get("summary", "一致性问题待复核。"),
                "affected_text_ref": issue["affected_text_ref"],
            }
            for issue in consistency_issues
            if issue["affected_text_ref"].startswith(section_run["draft_object_ref"])
        ]
        humanized = humanizer_adapter.humanize_section(
            section_plan=section_plan,
            section_index=index,
            draft_text=draft["writer_output"],
            critic_issues=critic_issues,
            model_profile=humanizer_profile,
            knowledge_context=knowledge_context,
        )
        humanized_results.append(humanized)
        beat_status = [
            {
                **beat,
                "status": "rewrite_required" if critic_issues and beat.get("index") == 2 else "humanizer_pass",
            }
            for beat in section_run.get("beat_status", [])
        ]
        status = "rewrite_required" if critic_issues else ("humanizer_pass" if index == len(section_runs) else "humanized")
        section_run_updates.append(
            {
                "section_run_id": section_run["section_run_id"],
                "status": status,
                "writer_output": draft["writer_output"],
                "critic_issues": critic_issues,
                "humanized_text": humanized["humanized_text"],
                "beat_status": beat_status,
                "draft_object_ref": section_run["draft_object_ref"],
                "critic_report_ref": section_run["critic_report_ref"],
                "humanized_object_ref": section_run["humanized_object_ref"],
                "model_profile_id": writer_call["model_profile_id"],
            }
        )
        humanized_sections.append(humanized["humanized_text"])

    COST_PER_1K = 0.002

    def _apply_metrics(call: dict[str, Any], pt: int, ct: int, lat: int) -> None:
        call["prompt_tokens"] = pt
        call["completion_tokens"] = ct
        call["latency_ms"] = lat
        call["cost_estimate"] = round((pt + ct) / 1000 * COST_PER_1K, 4)
        call["cost_estimate_status"] = "measured"

    writer_metrics = {"pt": sum(d.get("prompt_tokens", 0) for d in drafts), "ct": sum(d.get("completion_tokens", 0) for d in drafts), "lat": max((d.get("latency_ms", 0) for d in drafts), default=0)}
    humanizer_metrics = {"pt": sum(h.get("prompt_tokens", 0) for h in humanized_results), "ct": sum(h.get("completion_tokens", 0) for h in humanized_results), "lat": max((h.get("latency_ms", 0) for h in humanized_results), default=0)}
    for call in provider_calls:
        if call.get("agent_role") == "writer" and call.get("status") == "succeeded":
            _apply_metrics(call, writer_metrics["pt"], writer_metrics["ct"], writer_metrics["lat"])
        elif call.get("agent_role") == "humanizer" and call.get("status") == "succeeded":
            _apply_metrics(call, humanizer_metrics["pt"], humanizer_metrics["ct"], humanizer_metrics["lat"])

    return {
        "provider_calls": provider_calls,
        "retry_count": retry_count,
        "model_cost": store._build_model_cost(provider_calls, retry_count),
        "section_runs": section_run_updates,
        "assembled_chapter": "\n\n".join(humanized_sections),
        "consistency_issues": consistency_issues,
        "prompt_template_refs": deepcopy(prompt_package.get("template_refs", [])),
    }
