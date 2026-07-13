import json
import worker.llm_json as llm_json
from worker.llm_json import generate_json


def test_generate_json_returns_none_without_key(monkeypatch):
    monkeypatch.delenv("NOVELIST_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("NOVELIST_LLM_API_KEY", raising=False)
    assert generate_json("s", "u") is None


def test_generate_json_parses_model_response(monkeypatch):
    monkeypatch.setenv("NOVELIST_LLM_BASE_URL", "http://fake")
    monkeypatch.setenv("NOVELIST_LLM_API_KEY", "k")

    class FakeResp:
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False
        def read(self):
            return json.dumps({"choices": [{"message": {"content": '{"title": "开端"}'}}]}).encode("utf-8")

    monkeypatch.setattr(llm_json, "urlopen", lambda *a, **k: FakeResp())
    result = generate_json("s", "u")
    assert result == {"title": "开端"}


def test_generate_json_returns_none_on_bad_json(monkeypatch):
    monkeypatch.setenv("NOVELIST_LLM_BASE_URL", "http://fake")
    monkeypatch.setenv("NOVELIST_LLM_API_KEY", "k")

    class FakeResp:
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False
        def read(self):
            return json.dumps({"choices": [{"message": {"content": "not json"}}]}).encode("utf-8")

    monkeypatch.setattr(llm_json, "urlopen", lambda *a, **k: FakeResp())
    assert generate_json("s", "u") is None
