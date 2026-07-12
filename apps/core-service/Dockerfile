FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /workspace
COPY apps/core-service /workspace/apps/core-service
RUN pip install --no-cache-dir -e /workspace/apps/core-service

WORKDIR /workspace/apps/core-service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
