#!/bin/bash
set -e

echo "🔧 Generating .env from Codespaces secrets..."

# Only run in Codespaces
if [ "$CODESPACES" = "true" ]; then
  echo "Detected Codespaces environment."

  # Write resolved values into .env
  cat <<EOF > .env
SQL_SERVER_USER=${SQL_SERVER_USER_CODESPACES}
SQL_SERVER_PASSWORD=${SQL_SERVER_PASSWORD_CODESPACES}
SQL_SERVER_CONTAINER_SERVICE=${SQL_SERVER_CONTAINER_SERVICE_CODESPACES}
EOF

  echo "✅ .env file created."
else
  echo "⚠️ Not in Codespaces. Skipping .env generation."
fi

# Start Compose
docker compose up -d
