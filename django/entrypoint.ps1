
# Navigate to Django project directory
Set-Location -Path "tamprog"

# Run migrations
python manage.py migrate

# Start Celery worker in background
Start-Process -FilePath "celery" -ArgumentList "-A tamprog worker" -NoNewWindow

# Start Django server
python manage.py runserver 0.0.0.0:8000