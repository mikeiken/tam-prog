#!/bin/sh
# Run migrations
python manage.py migrate 
# Start Celery worker in background
celery -A tamprog worker &
# Start Django server
python manage.py runserver 0.0.0.0:8000 