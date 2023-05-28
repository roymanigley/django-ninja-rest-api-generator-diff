#!/bin/bash

echo "[+] LOCAL build started"
export APP_ENV='LOCAL'
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
export DJANGO_SUPERUSER_USERNAME='admin'
export DJANGO_SUPERUSER_PASSWORD='admin'
export DJANGO_SUPERUSER_EMAIL='admin@admin.local'
export DATABASE_URL='postgresql://dummy_user:dummy_pass@127.0.0.1/dummy'
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput || echo 'Superuser already exists'
echo "[+] LOCAL build completed"
