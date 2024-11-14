from django.contrib.auth import get_user_model
from .queries import *

# These \/ imports for the Celery
from celery import shared_task
from celery.result import AsyncResult
from django.forms.models import model_to_dict
from django.conf import settings

User = get_user_model()

class PersonService:
    @staticmethod
    def create_user(username, full_name, phone_number, password, wallet_balance=0.00):
        user = User.objects.create_user(
            username=username,
            full_name=full_name,
            phone_number=phone_number,
            password=password,
            wallet_balance=wallet_balance
        )
        return user

    @staticmethod
    def update_wallet_balance(user, amount):
        if user.wallet_balance is not None and user.wallet_balance >= amount:
            user.wallet_balance -= amount
            user.save(update_fields=['wallet_balance'])
            return True
        return False

@shared_task
def get_sorted_workers_task(sort_by: str = 'id', ascending: bool = True):
    if sort_by == 'id':
        query = GetWorkersSortedByID(ascending)
    elif sort_by == 'name':
        query = GetWorkersSortedByName(ascending)
    elif sort_by == 'price':
        query = GetWorkersSortedByPrice(ascending)
    elif sort_by == 'description':
        query = GetWorkersSortedByDescription(ascending)
    else:
        return []
    # Convert QuerySet to list of dictionaries
    queryset = query.execute()
    return [model_to_dict(field) for field in queryset]

class WorkerService:
    @staticmethod
    def get_sorted_workers(sort_by: str = 'price', ascending: bool = True):
        task = get_sorted_workers_task.delay('price', ascending)
        result = AsyncResult(task.id)
        return result.get(timeout=settings.DJANGO_ASYNC_TIMEOUT_S)