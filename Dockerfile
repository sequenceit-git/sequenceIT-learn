# ============================================================
# SkyLearn — Production Dockerfile
# ============================================================
# Stage 1: Builder — install all Python deps in an isolated layer
# Stage 2: Runtime — lean image with only what's needed to run
# ============================================================

# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies (needed for psycopg2, Pillow, lxml, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    zlib1g-dev \
    libxml2-dev \
    libxslt1-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements/production.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt


# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE="config.settings"

WORKDIR /app

# Install only runtime system libraries (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libjpeg62-turbo \
    libfreetype6 \
    libpng16-16 \
    libxml2 \
    libxslt1.1 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy project source code
COPY . /app/

# Create non-root user for security
RUN addgroup --system skylearn && \
    adduser --system --ingroup skylearn skylearn && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R skylearn:skylearn /app

# Copy and set up entrypoint script
RUN chmod +x /app/scripts/entrypoint.sh

USER skylearn

EXPOSE 8000

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
