FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /workspace
COPY apps/api-gateway /workspace/apps/api-gateway
RUN pip install --no-cache-dir -e /workspace/apps/api-gateway

WORKDIR /workspace/apps/api-gateway
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
