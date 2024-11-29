import random
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from conftest import fertilizers
from fertilizer.models import Fertilizer
from garden.models import Bed
from user.models import Worker
from user.services import PersonService
from .models import Order
from logging import getLogger
from garden.services import BedService
from plants.services import BedPlantService

log = getLogger(__name__)

class OrderService:
    @staticmethod
    def calculate_total_cost(field, plant, worker, beds_count):
        field_price = field.price * beds_count
        plant_price = plant.price * beds_count
        worker_price = worker.price
        total_cost = field_price + plant_price + worker_price
        log.debug(
            f"Total cost calculated: field={field_price}, plant={plant_price}, worker={worker_price}, total={total_cost}")
        return total_cost

    @staticmethod
    def create_order(user, field, plant, beds_count, comments, fertilize):
        available_workers = Worker.objects.all()
        if not available_workers.exists():
            log.warning("No available workers")
            return Response({'error': 'No available workers'}, status=status.HTTP_400_BAD_REQUEST)

        worker = random.choice(available_workers)

        if field.count_free_beds < beds_count:
            return Response({'error': 'Not enough free beds on the field'}, status=status.HTTP_400_BAD_REQUEST)

        total_cost = OrderService.calculate_total_cost(field, plant, worker, beds_count)
        if user.wallet_balance < total_cost:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

        rented_beds = []
        try:
            user.wallet_balance -= total_cost
            user.save()
            log.debug(f"User balance updated: {user.wallet_balance}")

            rented_beds = BedService.rent_beds(field, user, beds_count)
            log.debug(f"Rented beds count: {rented_beds}")
            if rented_beds != beds_count:
                raise ValueError("Failed to rent the required number of beds")

            fertilizer_used = fertilize
            fertilizer = None
            if fertilize:
                fertilizer = Fertilizer.objects.filter(compound__icontains=plant.name).first()
                if not fertilizer:
                    fertilizer_used = False
                    log.warning(f"No suitable fertilizer found for plant {plant.name}. Fertilization skipped.")

            plant_response = BedPlantService.plant_in_beds(
                field, plant, beds_count, fertilizer if fertilizer_used else None
            )
            if plant_response.status_code != 201:
                raise ValueError("Failed to plant in beds")

            completion_time = timezone.now() + timedelta(days=plant.growth_time)
            order = Order.objects.create(
                user=user,
                worker=worker,
                field=field,
                plant=plant,
                beds_count=beds_count,
                comments=comments,
                total_cost=total_cost,
                fertilize=fertilizer_used,
                completed_at=completion_time
            )
            log.debug(f"Order created successfully with ID={order.id}")

            response_message = {
                'status': 'Order created successfully',
                'order_id': order.id
            }
            if not fertilizer_used:
                response_message['warning'] = 'Fertilization skipped as no suitable fertilizer was found.'

            return Response(response_message, status=status.HTTP_201_CREATED)

        except Exception as e:
            log.error(f"Error creating order: {e}")
            if rented_beds:
                BedService.release_beds(field, len(rented_beds))
                log.debug(f"Released {len(rented_beds)} beds")
            user.wallet_balance += total_cost
            user.save()
            log.debug(f"User balance restored: {user.wallet_balance}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
