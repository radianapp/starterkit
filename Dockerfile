# ==============================================================================
# Multi-Stage Dockerfile untuk RDP Starter Kit
# Menggunakan package manager 'uv' untuk build ultra-cepat dan image minimalis
# ==============================================================================

# Stage 1: Build Dependencies
FROM python:3.12-slim AS builder

# Pasang uv binary dari image resmi Astral
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Environment untuk build Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install pustaka sistem yang dibutuhkan untuk build native extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Salin definisi dependensi dulu agar cache layer Docker optimal
COPY pyproject.toml uv.lock ./

# Install dependensi production (tanpa dev tools)
RUN uv sync --no-dev --frozen --no-install-project

# Salin seluruh source code proyek
COPY . .

# Install proyek ke virtualenv
RUN uv sync --no-dev --frozen

# ------------------------------------------------------------------------------
# Stage 2: Runtime Image (Minimalis & Aman)
FROM python:3.12-slim AS runtime

# Install pustaka runtime minimal (libpq untuk PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Buat user dan group non-root untuk keamanan kontainer
RUN groupadd -r django && useradd -r -g django -u 1000 django

WORKDIR /app

# Salin direktori aplikasi dan virtualenv dari builder stage
COPY --from=builder --chown=django:django /app /app

# Pastikan virtualenv ada di PATH
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=config.settings.production

# Buat direktori logs, media, dan staticfiles dengan hak akses user django
RUN mkdir -p /app/logs /app/media /app/staticfiles \
    && chown -R django:django /app/logs /app/media /app/staticfiles

USER django

EXPOSE 8000

# Default command untuk web: Gunicorn WSGI Server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "90", "--access-logfile", "-", "--error-logfile", "-"]
