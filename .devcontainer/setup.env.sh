#!/bin/bash
set -e

echo "🔧 Generating .env from Codespaces secrets..."

export SQL_SERVER_USER=$(echo $SQL_SERVER_USER_CODESPACES)
export SQL_SERVER_PASSWORD=$(echo $SQL_SERVER_PASSWORD_CODESPACES)
export SQL_SERVER_CONTAINER_SERVICE=$(echo $SQL_SERVER_CONTAINER_SERVICE_CODESPACES)

# Write resolved values into .env
echo "SQL_SERVER_USER=${SQL_SERVER_USER_CODESPACES}" > .env
echo "SQL_SERVER_PASSWORD=${SQL_SERVER_PASSWORD_CODESPACES}" >> .env
echo "SQL_SERVER_CONTAINER_SERVICE=${SQL_SERVER_CONTAINER_SERVICE_CODESPACES}" >> .env

# Start Compose
docker compose up -d
