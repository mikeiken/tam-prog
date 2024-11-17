#!/bin/sh
python manage.py migrate --verbosity 2 || true 
python manage.py auto_createsuperuser || true 
celery -A tamprog worker &
python manage.py runserver 0.0.0.0:8000 