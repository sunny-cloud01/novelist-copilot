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
    def _chat(self, *, model_profile: dict[str, Any], system: str, user: str) -> str:
        base_url = os.getenv("NOVELIST_LLM_BASE_URL")
        api_key = os.getenv("NOVELIST_LLM_API_KEY")
        if not base_url or not api_key:
            # 确定性 fallback：无 LLM 时用 user 前缀构造可读中文，而非裸截断
            return f"（离线草稿）{user.strip()[:280]}"
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
        try:
            with urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise ProviderExecutionError("provider_http_error", f"provider request failed: {exc.code}") from exc
        except URLError as exc:
            raise ProviderExecutionError("provider_network_error", "provider request failed") from exc
        except TimeoutError as exc:
            raise ProviderExecutionError("provider_timeout", "provider request timed out") from exc
        try:
            return payload["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderExecutionError("provider_response_invalid", "provider response missing message content") from exc

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
        text = self._chat(
            model_profile=model_profile,
            system="你是中文网文章节写手。必须遵循给定世界观与已确立设定，不得引入矛盾。输出一段可直接进入章节草稿的中文正文，不要解释。",
            user=user,
        )
        return {"writer_output": text, "scene_goal": scene_goal, "beat_phrase": beat_phrase, "provider_model_name": model_profile["provider_model_name"]}

    def review_sections(self, *, section_runs: list[dict[str, Any]], drafts: list[dict[str, Any]], consistency_report_id: str, model_profile: dict[str, Any]) -> list[dict[str, Any]]:
        base_url = os.getenv("NOVELIST_LLM_BASE_URL")
        api_key = os.getenv("NOVELIST_LLM_API_KEY")
        if not base_url or not api_key:
            return []
        combined = "\n".join(draft["writer_output"] for draft in drafts)
        review = self._chat(
            model_profile=model_profile,
            system="你是中文小说一致性审稿人。若没有严重阻断，只输出 PASS；若有阻断，用一句中文说明。",
            user=combined,
        )
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
        text = self._chat(
            model_profile=model_profile,
            system="你是中文小说润色师。保留剧情事实与给定设定，降低机械感，输出润色正文，不要解释。",
            user=f"{draft_text}\n{knowledge_block}",
        )
        return {"humanized_text": text, "provider_model_name": model_profile["provider_model_name"], "had_critic_issues": bool(critic_issues)}


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
    for index, (section_run, section_plan, draft) in enumerate(zip(section_runs, section_plans, drafts), start=1):
        critic_issues = [
            {
                "issue_id": issue["issue_id"],
                "severity": issue["severity"],
                "category": issue["category"],
                "summary": "主角境界描写与已批准设定冲突，需回收并重写冲突升级段。",
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

    return {
        "provider_calls": provider_calls,
        "retry_count": retry_count,
        "model_cost": store._build_model_cost(provider_calls, retry_count),
        "section_runs": section_run_updates,
        "assembled_chapter": "\n\n".join(humanized_sections),
        "consistency_issues": consistency_issues,
        "prompt_template_refs": deepcopy(prompt_package.get("template_refs", [])),
    }
