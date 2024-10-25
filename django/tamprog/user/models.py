from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')])
    account_number = models.CharField(max_length=20)
    full_name = models.CharField(max_length=255)

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)