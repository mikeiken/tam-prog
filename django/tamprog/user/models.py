from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator

class PersonManager(BaseUserManager):
    def create_user(self, username, full_name, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        user = self.model(username=username, full_name=full_name, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, full_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, full_name, phone_number, password, **extra_fields)

class Person(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = PersonManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    def __str__(self):
        return self.username
class Agronomist(models.Model):
    name = models.CharField(max_length=255)

class Worker(models.Model):
    name = models.CharField(max_length=255)
