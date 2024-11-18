./env-inject.ps1
python ./django/tamprog/manage.py migrate
python ./django/tamprog/manage.py createsuperuser