from django.db import models
from plants.models import BedPlant
from django.core.validators import EmailValidator, RegexValidator, MinValueValidator


class Fertilizer(models.Model):
    name = models.CharField(max_length=100)
    boost = models.IntegerField(validators=[MinValueValidator(0)])
    compound = models.CharField(max_length=1024)
    price = models.FloatField(default=0.00, validators=[MinValueValidator(0)])

class BedPlantFertilizer(models.Model):
    bed_plant = models.ForeignKey(BedPlant, on_delete=models.CASCADE)
    fertilizer = models.ForeignKey(Fertilizer, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
