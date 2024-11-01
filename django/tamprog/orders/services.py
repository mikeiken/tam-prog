from django.utils import timezone
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
    def create_order(user, worker, bed, plant, action):
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
