from django.utils import timezone
from .models import Order
from users.models import Worker
from fields.models import Bed
from plants.models import Plant

def create_order(user, worker, bed, plant, action):
    order = Order.objects.create(user=user, worker=worker, bed=bed, plant=plant, action=action)
    return order

def complete_order(order):
    order.completed_at = timezone.now()
    order.save()
    return order