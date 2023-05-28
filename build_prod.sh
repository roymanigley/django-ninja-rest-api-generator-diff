#!/bin/bash

echo "[+] PROD build started"
export APP_ENV='PROD'
pip install -r requirements.txt
export DJANGO_SUPERUSER_USERNAME="$APP_SUPERUSER_USERNAME"
export DJANGO_SUPERUSER_PASSWORD="$APP_SUPERUSER_PASSWORD"
export DJANGO_SUPERUSER_EMAIL="$APP_SUPERUSER_EMAIL"
export DJANGO_SECRET_KEY=$APP_SECRET_KEY
export DATABASE_URL=$APP_DATABASE_URL
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 manage.py createsuperuser --noinput || echo 'Superuser already exists'
echo "[+] PROD build completed"
        