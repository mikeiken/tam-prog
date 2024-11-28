from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from garden.services import BedService
from .models import BedPlant
from datetime import timedelta

@receiver(post_save, sender=BedPlant)
def check_growth_and_harvest_time(sender, instance, created, **kwargs):
    if not created:
        growth_end_date = instance.planted_at  + timedelta(days=instance.growth_time)
        if growth_end_date <= timezone.now() and not instance.is_grown:
            instance.is_grown = True
            instance.save()
            print(f"Растение на грядке {instance.bed.id} завершило рост.")

@receiver(post_save, sender=BedPlant)
def update_plant_growth(sender, instance, created, **kwargs):
    if instance.is_grown and not instance.is_harvested:
        instance.is_harvested = True
        instance.growth_percentage = 100
        instance.save()
        BedService.release_beds(instance.bed.field, 1)
        print(f"Растение на грядке {instance.bed.id} собрано и грядка освобождена.")