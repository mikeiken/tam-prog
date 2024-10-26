from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')])
    account_number = models.CharField(max_length=20)
    full_name = models.CharField(max_length=255)
    ROLE_CHOICES = (
        ('user', 'User'),
        ('worker', 'Worker'),
        ('agronomist', 'Agronomist'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Добавляем related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Добавляем related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Agronomist(models.Model):
    name = models.CharField(max_length=255)

class Worker(models.Model):
    name = models.CharField(max_length=255)
