#!/usr/bin/env bash
set -euo pipefail

# Wait for Postgres
if [ -n "${DATABASE_HOST:-}" ] && [ -n "${DATABASE_PORT:-}" ]; then
  echo "⏳ Waiting for Postgres at ${DATABASE_HOST}:${DATABASE_PORT}..."
  until nc -z "${DATABASE_HOST}" "${DATABASE_PORT}"; do
    sleep 0.5
  done
fi

# Wait for RabbitMQ
if [ -n "${CELERY_BROKER_URL:-}" ]; then
  # Parse host:port if amqp:// or amqps://
  # crude parse: amqp(s)://user:pass@host:port/vhost
  broker_host_port=$(python - <<'PY'
import os, urllib.parse
u = urllib.parse.urlparse(os.environ.get("CELERY_BROKER_URL",""))
if u.hostname and u.port:
    print(f"{u.hostname}:{u.port}")
PY
)
  if [ -n "$broker_host_port" ]; then
    host="${broker_host_port%:*}"
    port="${broker_host_port#*:}"
    echo "⏳ Waiting for RabbitMQ at ${host}:${port}..."
    until nc -z "$host" "$port"; do
      sleep 0.5
    done
  fi
fi

exec "$@"
