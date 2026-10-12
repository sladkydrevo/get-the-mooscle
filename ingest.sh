#!/usr/bin/env bash
set -a
source .env
set +a

echo "Creating database..."
mysql --host="$MYSQL__HOST" --port="$MYSQL__PORT" --user="$MYSQL__USER" --password="$MYSQL__PASSWORD" \
  -e "CREATE DATABASE IF NOT EXISTS $MYSQL__DATABASE;"

python -m db.create_schema
echo "Database schema created."

python -m db.ingest_data
echo "Data ingested."