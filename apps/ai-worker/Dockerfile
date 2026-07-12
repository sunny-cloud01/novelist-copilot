FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /workspace
COPY apps/ai-worker /workspace/apps/ai-worker
COPY apps/core-service /workspace/apps/core-service
RUN pip install --no-cache-dir -e /workspace/apps/ai-worker

WORKDIR /workspace/apps/ai-worker
CMD ["dramatiq", "worker.main", "--processes", "1", "--threads", "1"]
