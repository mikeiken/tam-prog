import random
from django.utils import timezone
from user.models import Worker
from user.services import PersonService
from .models import Order


class OrderService:
    @staticmethod
    def calculate_total_cost(bed, plant, worker):
        field_price = bed.field.price
        plant_price = plant.price
        worker_price = worker.price
        return field_price + plant_price + worker_price

    @staticmethod
    def create_order(user, bed, plant, action):
        available_workers = Worker.objects.all()
        if not available_workers.exists():
            return None
        worker = random.choice(available_workers)
        total_cost = OrderService.calculate_total_cost(bed, plant, worker)
        if PersonService.update_wallet_balance(user, total_cost):
            order = Order.objects.create(
                user=user,
                worker=worker,
                bed=bed,
                plant=plant,
                action=action,
                total_cost=total_cost
            )
            return order
        return None

    @staticmethod
    def complete_order(order):
        order.completed_at = timezone.now()
        order.save()
        return order

    @staticmethod
    def filter_orders(is_completed=None):
        if is_completed is not None:
            if is_completed:
                return Order.objects.filter(completed_at__isnull=False)
            else:
                return Order.objects.filter(completed_at__isnull=True)
        return Order.objects.all()
