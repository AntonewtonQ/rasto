FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir "Django>=5.2,<5.3" "django-allauth[mfa]>=65,<66" "django-axes>=8,<10" \
    "django-csp>=4,<5" "argon2-cffi>=23" "psycopg[binary]>=3.2,<4" "whitenoise>=6.7" "gunicorn>=22" \
    "djangorestframework>=3.15,<4" "drf-spectacular>=0.27"
COPY manage.py ./
COPY config ./config
COPY rasto ./rasto
COPY templates ./templates
RUN DJANGO_SECRET_KEY=build-only python manage.py collectstatic --noinput
RUN useradd -r -u 1000 app && mkdir -p /app/media && chown app /app/media
USER app
EXPOSE 8000
