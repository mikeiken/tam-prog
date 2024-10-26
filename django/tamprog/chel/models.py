from django.db import models
from django.core.validators import RegexValidator

class Person(models.Model):
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^+?1?d{9,15}$')])

class Agronomist(models.Model):
    name = models.CharField(max_length=255)

class Worker(models.Model):
    name = models.CharField(max_length=255)
