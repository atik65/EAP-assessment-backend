#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
mkdir -p logs
python manage.py migrate


# start command 
# gunicorn root_app.wsgi:application