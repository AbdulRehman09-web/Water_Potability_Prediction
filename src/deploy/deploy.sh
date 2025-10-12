#!/usr/bin/env bash
set -e

# Simple local deployment via docker-compose
# Make sure docker and docker-compose are installed and running.

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_FILE="${BASE_DIR}/deploy/docker-compose.yml"

echo "Deploy script running from ${BASE_DIR}"

# Build and start containers
docker compose -f "${COMPOSE_FILE}" pull || true
docker compose -f "${COMPOSE_FILE}" build --pull
docker compose -f "${COMPOSE_FILE}" up -d

echo "Deployment complete."
echo "Frontend available at: http://localhost:8501"
echo "Backend health: http://localhost:8000/health"