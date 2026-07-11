from typing import Any


def success_envelope(data: dict[str, Any], request_id: str, trace_id: str) -> dict[str, Any]:
    return {
        "data": data,
        "meta": {
            "request_id": request_id,
            "trace_id": trace_id,
        },
        "errors": [],
    }
