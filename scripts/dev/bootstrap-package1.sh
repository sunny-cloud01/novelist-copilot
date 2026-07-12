#!/usr/bin/env bash
set -euo pipefail

docker compose -f infra/docker-compose.yml up -d --build postgres redis minio minio-bootstrap core-service api-gateway ai-worker scheduler
docker compose -f infra/docker-compose.yml ps
