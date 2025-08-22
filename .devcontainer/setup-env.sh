#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Starting setup-env.sh..."

trap 'echo "❌ setup-env.sh failed at line $LINENO"; exit 1' ERR

# Detect environment
IS_CODESPACES=${CODESPACES:-false}
IS_CI=${CI:-false}
IS_DEVCONTAINER=false

if grep -q "devcontainer" /proc/1/cgroup || [[ "$PWD" == "/workspaces/"* ]]; then
  IS_DEVCONTAINER=true
fi

echo "🌐 Environment detection:"
echo "  - CODESPACES: $IS_CODESPACES"
echo "  - CI:         $IS_CI"
echo "  - DEVCONTAINER: $IS_DEVCONTAINER"

# Map secrets based on environment
if [[ "$IS_CODESPACES" == "true" || "$IS_DEVCONTAINER" == "true" ]]; then
  SQL_SERVER_USER=${SQL_SERVER_USER_CODESPACES:-""}
  SQL_SERVER_PASSWORD=${SQL_SERVER_PASSWORD_CODESPACES:-""}
  SQL_SERVER_CONTAINER_SERVICE=${SQL_SERVER_CONTAINER_SERVICE_CODESPACES:-""}
elif [[ "$IS_CI" == "true" ]]; then
  SQL_SERVER_USER=${SQL_SERVER_USER_CI:-""}
  SQL_SERVER_PASSWORD=${SQL_SERVER_PASSWORD_CI:-""}
  SQL_SERVER_CONTAINER_SERVICE=${SQL_SERVER_CONTAINER_SERVICE_CI:-""}
else
  # Local fallback (e.g., from .secrets file)
  if [[ -f .secrets ]]; then
    source .secrets
  fi
  SQL_SERVER_USER=${SQL_SERVER_USER:-""}
  SQL_SERVER_PASSWORD=${SQL_SERVER_PASSWORD:-""}
  SQL_SERVER_CONTAINER_SERVICE=${SQL_SERVER_CONTAINER_SERVICE:-"localhost"}
fi

# Fail fast if required secrets are missing
: "${SQL_SERVER_USER:?❌ SQL_SERVER_USER is not set}"
: "${SQL_SERVER_PASSWORD:?❌ SQL_SERVER_PASSWORD is not set}"
: "${SQL_SERVER_CONTAINER_SERVICE:?❌ SQL_SERVER_CONTAINER_SERVICE is not set}"

if [[ -z "${SQL_SERVER_USER:-}" || -z "${SQL_SERVER_PASSWORD:-}" || -z "${SQL_SERVER_CONTAINER_SERVICE:-}" ]]; then
  echo "⚠️ Required secrets missing. Skipping .env generation."
  exit 0
fi

# Construct SQLAlchemy URI
SQLALCHEMY_DATABASE_URI="mssql+pyodbc://${SQL_SERVER_USER}:${SQL_SERVER_PASSWORD}@${SQL_SERVER_CONTAINER_SERVICE}:1433/lookout?driver=ODBC+Driver+18+for+SQL+Server"

# Write to .env
cat <<EOF > .env
SQLALCHEMY_DATABASE_URI=${SQLALCHEMY_DATABASE_URI}
FLASK_ENV=development
EOF

echo "✅ .env generated:"
cat .env
