from django.db import models
from user.models import User

class Field(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Bed(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    is_rented = models.BooleanField(default=False)
    rented_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
