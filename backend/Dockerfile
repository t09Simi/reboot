# syntax=docker/dockerfile:1
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files at build time for WhiteNoise. Dummy env vars are only
# used during build; real values from Render override at runtime.
ENV SECRET_KEY=dummy-for-build \
    DATABASE_URL=sqlite:///dummy.db
RUN python manage.py collectstatic --noinput
ENV SECRET_KEY="" \
    DATABASE_URL=""

RUN useradd --create-home --uid 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Run migrations then start gunicorn. 1 worker + 2 threads is right-sized
# for Render's free tier (512MB RAM).
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn reboot.wsgi:application --bind 0.0.0.0:8000 --workers 1 --threads 2"]