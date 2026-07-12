FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /workspace
COPY apps/scheduler /workspace/apps/scheduler
COPY apps/ai-worker /workspace/apps/ai-worker
COPY apps/core-service /workspace/apps/core-service
RUN pip install --no-cache-dir -e /workspace/apps/scheduler

WORKDIR /workspace/apps/scheduler
CMD ["python", "-m", "scheduler.main"]
