#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Starting setup-env.sh..."

trap 'echo "❌ setup-env.sh failed at line $LINENO"; exit 1' ERR

# ─────────────────────────────────────────────────────────────
# 🧠 Environment Detection
# ─────────────────────────────────────────────────────────────
IS_CODESPACES=${CODESPACES:-false}
IS_CI=${CI:-false}
IS_GITHUB_RUNNER=${GITHUB_ACTIONS:-false}
IS_DEVCONTAINER=false

if grep -q "devcontainer" /proc/1/cgroup || [[ "$PWD" == "/workspaces/"* ]]; then
  IS_DEVCONTAINER=true
fi

if [[ "$IS_CODESPACES" == "true" ]]; then
  ENVIRONMENT="codespaces"
elif [[ "$IS_CI" == "true" || "$IS_GITHUB_RUNNER" == "true" || "$IS_DEVCONTAINER" == "true" ]]; then
  ENVIRONMENT="ci"
else
  ENVIRONMENT="local"
fi

echo "🌐 Detected environment: $ENVIRONMENT"

# ─────────────────────────────────────────────────────────────
# 🔐 Secret Resolution Function
# ─────────────────────────────────────────────────────────────
resolve_secret() {
  local base_name=$1
  local fallback=$2
  local value=""

  case "$ENVIRONMENT" in
    codespaces)
      value="${base_name}_CODESPACES"
      ;;
    ci)
      value="${base_name}_CI"
      [[ -z "${!value:-}" ]] && value="${base_name}_CODESPACES"
      ;;
    local)
      [[ -f .secrets ]] && source .secrets
      value="$base_name"
      ;;
  esac

  echo "${!value:-$fallback}"
}

# ─────────────────────────────────────────────────────────────
# 🧪 Resolve Secrets
# ─────────────────────────────────────────────────────────────
SQL_SERVER_USER=$(resolve_secret SQL_SERVER_USER "")
SQL_SERVER_PASSWORD=$(resolve_secret SQL_SERVER_PASSWORD "")
SQL_SERVER_CONTAINER_SERVICE=$(resolve_secret SQL_SERVER_CONTAINER_SERVICE "sqlserver")

# ─────────────────────────────────────────────────────────────
# 🚨 Validate Secrets
# ─────────────────────────────────────────────────────────────
echo "🔍 Secret summary:"
echo "  - SQL_SERVER_USER: ${SQL_SERVER_USER:+[set]}"
echo "  - SQL_SERVER_PASSWORD: ${SQL_SERVER_PASSWORD:+[set]}"
echo "  - SQL_SERVER_CONTAINER_SERVICE: $SQL_SERVER_CONTAINER_SERVICE"

: "${SQL_SERVER_USER:?❌ SQL_SERVER_USER is not set}"
: "${SQL_SERVER_PASSWORD:?❌ SQL_SERVER_PASSWORD is not set}"
: "${SQL_SERVER_CONTAINER_SERVICE:?❌ SQL_SERVER_CONTAINER_SERVICE is not set}"

# ─────────────────────────────────────────────────────────────
# 🧼 Guard .env Regeneration
# ─────────────────────────────────────────────────────────────
if [[ -f .env && "${FORCE_REGEN:-false}" != "true" ]]; then
  echo "⚠️ .env already exists. Skipping regeneration."
  exit 0
fi

echo "🔍 SQL_SERVER_USER: ${SQL_SERVER_USER:-[unset]}"
echo "🔍 SQL_SERVER_PASSWORD: ${SQL_SERVER_PASSWORD:+[set]}"
echo "🔍 SQL_SERVER_CONTAINER_SERVICE: ${SQL_SERVER_CONTAINER_SERVICE:-[unset]}"





# ─────────────────────────────────────────────────────────────
# 🧪 Construct SQLAlchemy URI and Write .env
# ─────────────────────────────────────────────────────────────
SQLALCHEMY_DATABASE_URI="mssql+pyodbc://${SQL_SERVER_USER}:${SQL_SERVER_PASSWORD}@${SQL_SERVER_CONTAINER_SERVICE}:1433/lookout?driver=ODBC+Driver+18+for+SQL+Server"

if [[ -n "${SQLALCHEMY_DATABASE_URI:-}" ]]; then
  echo "🔍 SQLALCHEMY_DATABASE_URI: ${SQLALCHEMY_DATABASE_URI}"
else
  echo "⚠️ SQLALCHEMY_DATABASE_URI is not set"
fi

echo "🔍 Full SQLAlchemy URI: $SQLALCHEMY_DATABASE_URI"


cat <<EOF > .env
SQLALCHEMY_DATABASE_URI=${SQLALCHEMY_DATABASE_URI}
FLASK_ENV=development
EOF

echo "✅ .env generated:"
cat .env