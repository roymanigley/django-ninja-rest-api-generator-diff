#!/bin/bash

echo "[+] starting app dummy locally"
export APP_ENV='TEST'
source .env/bin/activate
export DATABASE_URL='sqlite://database.sqlite'
python ./manage.py test
