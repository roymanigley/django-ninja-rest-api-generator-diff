#!/bin/bash

echo "[+] starting app dummy productive"
export APP_ENV='PROD'
export DJANGO_SECRET_KEY=$APP_SECRET_KEY
gunicorn dummy_project.wsgi:application
        