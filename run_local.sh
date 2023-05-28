#!/bin/bash

echo "[+] starting app dummy locally"
export APP_ENV='LOCAL'
source .env/bin/activate
export DATABASE_URL='postgresql://dummy_user:dummy_pass@127.0.0.1/dummy'
python ./manage.py runserver
