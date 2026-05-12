# syntax=docker/dockerfile:1

# Base image — slim variant, ~130MB instead of ~1GB
FROM python:3.14-slim

# Don't buffer stdout/stderr, don't write .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Working directory inside the container
WORKDIR /app

# Install Python dependencies first (caches well across rebuilds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user and give it ownership of /app
RUN useradd --create-home --uid 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Document the port the app listens on
EXPOSE 8000

# Production server — gunicorn, NOT runserver
CMD ["gunicorn", "reboot.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]