from django.db import models
from django.core.validators import EmailValidator, RegexValidator, MinValueValidator

#агроном, поставщик, пользователь, грядка, растение, удобрение, работник, участок, заказ

class Agronomist(models.Model):
    #зп, дни работы, график работы
    salary = models.IntegerField(validators=[MinValueValidator(0)])
    days_work = models.CharField(max_length=1024)
    work_schedule = models.CharField(max_length=1024)

class Supplier(models.Model):
    #почта, данные для оплаты-номер счета
    email_validator = EmailValidator(allowlist=["mail.ru", "gmail.com", "yahoo.com", "yandex.ru"])
    email = models.CharField(max_length=1024, unique=True, validators=[email_validator])
    account_number = models.CharField(max_length=20, unique=True)

class Worker(models.Model):
    #должность, зп, дни работы, график работы
    job_title = models.CharField(max_length=1024)
    salary = models.IntegerField(validators=[MinValueValidator(0)])
    days_work = models.CharField(max_length=1024)
    work_schedule = models.CharField(max_length=1024)

class GardenBed(models.Model):
    #состояние, размер, цена
    state =models.CharField(max_length=1024)
    size = models.FloatField(validators=[MinValueValidator(0.0)])
    price = models.FloatField(validators=[MinValueValidator(0.0)])

class Fertilizer(models.Model):
    #название, цена, то на сколько ускоряет рост, состав
    name = models.CharField(max_length=1024)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    boost =models.IntegerField(validators=[MinValueValidator(0)])
    compound = models.CharField(max_length=1024)

class User(models.Model):
    #хеш пароля, логин, роль, почта, номер телефона, внешний ключ на id агронома, внешний ключ на id работника
    password = models.CharField(max_length=1024)
    login = models.CharField(max_length=1024, unique=True)
    role = models.CharField(max_length=1024)

    email_validator = EmailValidator(allowlist = ["mail.ru", "gmail.com", "yahoo.com", "yandex.ru"])
    email = models.CharField(max_length=1024, unique=True, validators=[email_validator])

    phone_validator = RegexValidator(regex=r'^+7d{10}$')
    phone = models.CharField(max_length=18, unique=True, validators=[phone_validator])

    agronomist_id = models.ForeignKey(Agronomist,verbose_name='agronomist_id', on_delete=models.PROTECT)
    worker_id = models.ForeignKey(Worker, verbose_name='worker_id', on_delete=models.PROTECT)

class Plant(models.Model):
    #название, цена, время роста, описание, дата посадки, внешний ключ на id грядки
    name = models.CharField(max_length=1024)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    growth_time = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.CharField(max_length=1024)
    landing_data = models.DateField()
    garden_id = models.ForeignKey(GardenBed, verbose_name='garden_id', on_delete=models.CASCADE)


class Plot(models.Model):
    #внешний ключ на id грядку, размер
    size = models.FloatField(validators=[MinValueValidator(0.0)])
    garden_id = models.ForeignKey(GardenBed, verbose_name='garden_id', on_delete=models.CASCADE)


class Order(models.Model):
    #срок,внешний ключ на id грядку, внешний ключ на id растение, внешний ключ на id работник, внешний ключ на id удобрение
    deadline = models.DateField()
    garden_id = models.ForeignKey(GardenBed, verbose_name='garden_id', on_delete=models.PROTECT)
    plant_id = models.ForeignKey(Plant, verbose_name='plant_id', on_delete=models.PROTECT)
    worker_id = models.ForeignKey(Worker, verbose_name='worker_id', on_delete=models.PROTECT)
    fertilizer_id = models.ForeignKey(Fertilizer, verbose_name='fertilizer_id', on_delete=models.PROTECT)


class AvailablePlants(models.Model):
    #название, цена, время роста, описание, дата посадки, грядка
    name = models.CharField(max_length=1024)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    growth_time = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.CharField(max_length=1024)
    landing_data = models.DateField()
    garden_id = models.IntegerField(default=0)