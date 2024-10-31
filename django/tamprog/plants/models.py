from email.policy import default

from django.db import models
from garden.models import Bed

class Plant(models.Model):
    name = models.CharField(max_length=100)
    growth_time = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class BedPlant(models.Model):
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    planted_at = models.DateTimeField(auto_now_add=True)
    fertilizer_applied = models.BooleanField(default=False)
    growth_time = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.growth_time = self.plant.growth_time
        super().save(*args, **kwargs)