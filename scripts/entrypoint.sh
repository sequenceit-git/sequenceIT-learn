#!/bin/bash
# ============================================================
# SkyLearn — Docker Entrypoint Script
# Runs on every container start before Gunicorn launches.
# ============================================================

set -e

echo "============================================================"
echo "  SkyLearn Entrypoint — $(date)"
echo "============================================================"

# ----------------------------------------------------------
# Wait for PostgreSQL to be ready
# ----------------------------------------------------------
if [ "$DB_ENGINE" = "django.db.backends.postgresql" ]; then
    echo ">>> Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
    
    MAX_RETRIES=30
    RETRY_COUNT=0
    until nc -z "$DB_HOST" "$DB_PORT"; do
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
            echo "ERROR: PostgreSQL did not become available after $MAX_RETRIES attempts. Exiting."
            exit 1
        fi
        echo "  PostgreSQL not ready yet (attempt $RETRY_COUNT/$MAX_RETRIES). Waiting 2s..."
        sleep 2
    done
    echo ">>> PostgreSQL is ready!"
fi

# ----------------------------------------------------------
# Apply database migrations
# ----------------------------------------------------------
echo ">>> Running database migrations..."
python manage.py migrate --noinput

# ----------------------------------------------------------
# Collect static files
# ----------------------------------------------------------
echo ">>> Collecting static files..."
python manage.py collectstatic --noinput --clear

# ----------------------------------------------------------
# Start Gunicorn
# ----------------------------------------------------------
echo ">>> Starting Gunicorn..."
exec "$@"
