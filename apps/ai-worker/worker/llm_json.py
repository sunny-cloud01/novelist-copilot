from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _strip_fence(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def generate_json(system: str, user: str, model_name: str = "deepseek-chat") -> dict[str, Any] | None:
    base_url = os.getenv("NOVELIST_LLM_BASE_URL")
    api_key = os.getenv("NOVELIST_LLM_API_KEY")
    if not base_url or not api_key:
        return None
    endpoint = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": model_name,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.5,
        "max_tokens": 1200,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")
    request = Request(
        endpoint,
        data=body,
        headers={"authorization": f"Bearer {api_key}", "content-type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
        content = payload["choices"][0]["message"]["content"]
        parsed = json.loads(_strip_fence(content))
        return parsed if isinstance(parsed, dict) else None
    except (HTTPError, URLError, TimeoutError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        return None
