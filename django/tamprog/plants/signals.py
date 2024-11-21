from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BedPlant
from .services import BedPlantService

from rest_framework.response import Response
from rest_framework import status
from garden.services import BedService  # Сервис для работы с грядками
from orders.services import OrderService  # Сервис для работы с заказами
from orders.models import Order

@receiver(post_save, sender=BedPlant)
def check_growth_and_harvest(sender, instance, created, **kwargs):
    if created:
        return
    """if instance.is_grown and not instance.is_harvested:
        BedPlantService.check_and_harvest_plant(instance)
        BedPlantService.dig_up_plant(instance)"""
    if instance.is_grown and not instance.is_harvested:  # Если растение выросло, но не было собрано
        # Завершаем заказ
        if instance.bed.is_rented:
            try:
                order = Order.objects.get(bed=instance.bed, completed_at__isnull=True)
                OrderService.complete_order(order)  # Завершаем заказ
            except Order.DoesNotExist:
                pass  # Если нет активного заказа, пропускаем

        # Освобождаем грядку
        response = BedService.release_bed(instance.bed.id)
        if isinstance(response, Response) and response.status_code == status.HTTP_200_OK:
            # Если релиз грядки прошел успешно, выкапываем растение
            instance.is_harvested = True
            instance.save(update_fields=['is_harvested'])
            # Вызываем функцию выкапывания растения
            BedPlantService.dig_up_plant(instance)


