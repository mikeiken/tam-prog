from django.db import models
from user.models import Person
from django.core.validators import MinValueValidator

class Field(models.Model):
    name = models.CharField(max_length=100)
    count_free_beds = models.IntegerField(default=0)
    all_beds = models.IntegerField(default=0)
    price = models.FloatField(default=0.00, validators=[MinValueValidator(0)])

class Bed(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    is_rented = models.BooleanField(default=False)
    rented_by = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL)


