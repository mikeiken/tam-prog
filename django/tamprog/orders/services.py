import random
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from user.models import Worker
from user.services import PersonService
from .models import Order
from logging import getLogger
from garden.services import BedService
from plants.services import BedPlantService

log = getLogger(__name__)


from django.db import transaction  # Для атомарности операций

class OrderService:
    @staticmethod
    def calculate_total_cost(bed, plant, worker):
        field_price = bed.field.price
        plant_price = plant.price
        worker_price = worker.price
        total_cost = field_price + plant_price + worker_price
        log.debug(
            f"Total cost calculated: bed={field_price}, plant={plant_price}, worker={worker_price}, total={total_cost}")
        return total_cost

    @staticmethod
    def create_order(user, bed, plant, comments):
        available_workers = Worker.objects.all()
        if not available_workers.exists():
            log.warning("No available workers")
            return Response(
                {'error': 'No available workers'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Выбор рабочего
        worker = random.choice(available_workers)
        total_cost = OrderService.calculate_total_cost(bed, plant, worker)

        # Проверка баланса пользователя
        if user.wallet_balance < total_cost:
            return Response(
                {'error': 'Insufficient funds'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Списание средств
        user.wallet_balance -= total_cost
        user.save()

        try:
            # Создание заказа
            order = Order.objects.create(
                user=user,
                worker=worker,
                bed=bed,
                plant=plant,
                comments=comments,
                total_cost=total_cost
            )

            # Аренда грядки
            rent_response = BedService.rent_bed(bed.id, user)
            if rent_response.status_code != 200:
                raise Exception("Failed to rent bed")

            # Посадка растения
            plant_response = BedPlantService.plant_in_bed(bed, plant)
            if plant_response.status_code != 201:
                raise Exception(plant_response.data.get("error", "Failed to plant in bed"))

            log.debug(f"Order created successfully with ID={order.id}")
            return Response(
                {'status': 'Order created successfully', 'order_id': order.id},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            log.error(f"Error creating order: {e}")

            # Возврат средств пользователю
            user.wallet_balance += total_cost
            user.save()

            # Откат аренды грядки (если была выполнена)
            BedService.release_bed(bed.id)

            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
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
