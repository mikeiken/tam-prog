from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BedPlant
from .services import BedPlantService

from rest_framework.response import Response
from rest_framework import status
from garden.services import BedService
from orders.services import OrderService
from orders.models import Order

@receiver(post_save, sender=BedPlant)
def check_growth_and_harvest(sender, instance, created, **kwargs):
    if created:
        return
    if instance.is_grown and not instance.is_harvested:
        if instance.bed.is_rented:
            try:
                order = Order.objects.get(bed=instance.bed, completed_at__isnull=True)
                OrderService.complete_order(order)
            except Order.DoesNotExist:
                pass

        response = BedService.release_bed(instance.bed.id)
        if isinstance(response, Response) and response.status_code == status.HTTP_200_OK:
            instance.is_harvested = True
            instance.save(update_fields=['is_harvested'])
            BedPlantService.dig_up_plant(instance)


