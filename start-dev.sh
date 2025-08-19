#!/bin/bash

# This script is not used at this time
# it's purpose wast to create a delay for entering the sql sa password
# and to wait for the .env.ready file to be created

set -e

# Wait for .env.ready
while [ ! -f .env.ready ]; do
  echo "⏳ Waiting for .env.ready..."
  sleep 1
done

# Validate .env
source .env
if [ -z "$SQL_SERVER_PASSWORD" ]; then
  echo "❌ SQL_SERVER_PASSWORD not set. Aborting."
  exit 1
fi

# Start SQL Server container
# docker compose up -d sqlserver

echo "Waiting for SQL Server to be ready..."
until nc -z sqlserver 1433; do
  sleep 1
done
echo "SQL Server is up!"
