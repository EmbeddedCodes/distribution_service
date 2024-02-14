#!/bin/sh

python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input
# Start RQ worker
python manage.py rqworker default &

# Start Gunicorn server
gunicorn frozen_dessert.wsgi:application --bind 0.0.0.0:8000






