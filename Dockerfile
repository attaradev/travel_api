# Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=1

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential curl netcat-traditional gcc libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Install deps early for caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Add project
COPY . /app

# Default envs (overridden by compose .env)
ENV DJANGO_SETTINGS_MODULE=core.settings \
  PYTHONPATH=/app

# Entrypoint
COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]

# start server
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
