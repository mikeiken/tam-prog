from django.db import models
from garden.models import Bed
from django.utils import timezone
from django.core.validators import MinValueValidator

class Plant(models.Model):
    name = models.CharField(max_length=100)
    growth_time = models.IntegerField(default=0)
    price = models.FloatField(default=0.00, validators=[MinValueValidator(0)])
    description = models.TextField()

class BedPlant(models.Model):
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    planted_at = models.DateTimeField(auto_now_add=True)
    fertilizer_applied = models.BooleanField(default=False)
    growth_time = models.IntegerField(default=1)
    is_harvested = models.BooleanField(default=False)
    growth_percentage = models.IntegerField(default=0)  # Используем обычное поле для хранения процента роста

    @property
    def remaining_growth_time(self):
        elapsed_time = (timezone.now() - self.planted_at).days
        remaining_time = self.growth_time - elapsed_time
        return max(0, remaining_time)

    @property
    def is_grown(self):
        return self.remaining_growth_time == 0

    @property
    def growth_percentage_calculated(self):
        elapsed_time = (timezone.now() - self.planted_at).days
        percentage = (elapsed_time / self.growth_time) * 100
        return min(max(percentage, 0), 100)