from django.db import models
from garden.models import Bed

class Plant(models.Model):
    name = models.CharField(max_length=100)
    growth_time = models.IntegerField()  # in days
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class BedPlant(models.Model):
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    planted_at = models.DateTimeField(auto_now_add=True)
    fertilizer_applied = models.BooleanField(default=False)