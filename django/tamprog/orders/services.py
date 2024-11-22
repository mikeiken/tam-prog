import random
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from user.models import Worker
from user.services import PersonService
from .models import Order
from logging import getLogger

log = getLogger(__name__)

class OrderService:
    @staticmethod
    def calculate_total_cost(bed, plant, worker):
        field_price = bed.field.price
        plant_price = plant.price
        worker_price = worker.price
        log.debug(f"Total cost calculated: {field_price + plant_price + worker_price}")
        return field_price + plant_price + worker_price

    @staticmethod
    def create_order(user, bed, plant, action):
        available_workers = Worker.objects.all()
        if not available_workers.exists():
            log.warning("No available workers")
            return Response(
                {'error': 'No available workers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        worker = random.choice(available_workers)
        total_cost = OrderService.calculate_total_cost(bed, plant, worker)
        wallet_response = PersonService.update_wallet_balance(user, total_cost)
        if wallet_response.status_code != status.HTTP_200_OK:
            log.warning(f"Insufficient funds for user with ID={user.id}")
            return wallet_response

        order = Order.objects.create(
            user=user,
            worker=worker,
            bed=bed,
            plant=plant,
            action=action,
            total_cost=total_cost
        )
        log.debug(f"Order created with ID={order.id}")
        return Response(
            {'status': 'Order created successfully', 'order_id': order.id},
            status=status.HTTP_201_CREATED
        )

    @staticmethod
    def complete_order(order):
        order.completed_at = timezone.now()
        order.save()
        log.debug(f"Order with ID={order.id} completed")
        return order

    @staticmethod
    def filter_orders(is_completed=None):
        if is_completed is not None:
            if is_completed:
                log.debug("Filtering completed orders")
                return Order.objects.filter(completed_at__isnull=False)
            else:
                log.debug("Filtering not completed orders")
                return Order.objects.filter(completed_at__isnull=True)
        log.debug("Getting all orders")
        return Order.objects.all()
