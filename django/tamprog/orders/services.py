import random
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from user.models import Worker
from user.services import PersonService
from .models import Order
from garden.services import BedService
from plants.services import BedPlantService


class OrderService:
    @staticmethod
    def calculate_total_cost(bed, plant, worker):
        field_price = bed.field.price
        plant_price = plant.price
        worker_price = worker.price
        return field_price + plant_price + worker_price

    @staticmethod
    def create_order(user, bed, plant, comments):

        available_workers = Worker.objects.all()
        if not available_workers.exists():
            return Response(
                {'error': 'No available workers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        worker = random.choice(available_workers)

        total_cost = OrderService.calculate_total_cost(bed, plant, worker)

        order = Order.objects.create(
            user=user,
            worker=worker,
            bed=bed,
            plant=plant,
            comments=comments,
            total_cost=total_cost
        )
        rent_response = BedService.rent_bed(bed.id, user)
        if rent_response.status_code != 200:
            return rent_response

        plant_response = BedPlantService.plant_in_bed(bed, plant)
        if plant_response.status_code != 200:
            return plant_response

        wallet_response = PersonService.update_wallet_balance(user, total_cost)
        if wallet_response.status_code != status.HTTP_200_OK:
            return wallet_response

        return Response(
            {'status': 'Order created successfully', 'order_id': order.id},
            status=status.HTTP_201_CREATED
        )


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
