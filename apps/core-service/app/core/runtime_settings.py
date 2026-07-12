from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class RuntimeSettings:
    postgres_url: str
    redis_url: str
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str
    core_service_url: str | None = None


def load_runtime_settings() -> RuntimeSettings:
    return RuntimeSettings(
        postgres_url=os.getenv("NOVEL_FACTORY_POSTGRES_URL", "postgresql://novel:novel@localhost:5436/novel_factory"),
        redis_url=os.getenv("NOVEL_FACTORY_REDIS_URL", "redis://localhost:6379/0"),
        minio_endpoint=os.getenv("NOVEL_FACTORY_MINIO_ENDPOINT", "http://localhost:9000"),
        minio_access_key=os.getenv("NOVEL_FACTORY_MINIO_ACCESS_KEY", "novel-factory"),
        minio_secret_key=os.getenv("NOVEL_FACTORY_MINIO_SECRET_KEY", "replace-me"),
        minio_bucket=os.getenv("NOVEL_FACTORY_MINIO_BUCKET", "novel-factory-dev"),
        core_service_url=os.getenv("NOVEL_FACTORY_CORE_SERVICE_URL"),
    )
