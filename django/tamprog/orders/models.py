from django.db import models
from user.models import Person, Worker
from garden.models import Bed
from plants.models import Plant
from django.core.validators import MinValueValidator

class Order(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    comments = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_cost = models.FloatField(default=0.00, validators=[MinValueValidator(0)])