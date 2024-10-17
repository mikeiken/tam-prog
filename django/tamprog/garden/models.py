from django.db import models


#агроном, поставщик, пользователь, грядка, растение, удобрение, работник, участок, заказ

class Agronomist(models.Model):
    #зп, дни работы, график работы
    salary = models.IntegerField()
    days_work = models.CharField(max_length=1024)
    work_schedule = models.CharField(max_length=1024)

class Supplier(models.Model):
    #почта, данные для оплаты-номер счета
    email = models.CharField(max_length=1024)
    account_number = models.CharField(max_length=1024)

class Worker(models.Model):
    #должность, зп, дни работы, график работы
    job_title = models.CharField(max_length=1024)
    salary = models.IntegerField()
    days_work = models.CharField(max_length=1024)
    work_schedule = models.CharField(max_length=1024)

class GardenBed(models.Model):
    #состояние, размер
    state =models.CharField(max_length=1024)
    size = models.FloatField()

class Fertilizer(models.Model):
    #название,состав
    name = models.CharField(max_length=1024)
    compound = models.CharField(max_length=1024)

class User(models.Model):
    #хеш пароля, логин, роль, почта, номер телефона, внешний ключ на id агронома, внешний ключ на id работника
    password = models.CharField(max_length=1024)
    login = models.CharField(max_length=1024)
    role = models.CharField(max_length=1024)
    email = models.CharField(max_length=1024)
    phone = models.CharField(max_length=18)
    agronomist_id = models.ForeignKey(Agronomist,verbose_name='agronomist_id', on_delete=models.PROTECT)
    worker_id = models.ForeignKey(Worker, verbose_name='worker_id', on_delete=models.PROTECT)

class Plant(models.Model):
    #название, условия роста, необходимые питательные вещества, внешний ключ на id грядки
    name = models.CharField(max_length=1024)
    growth_conditions = models.CharField(max_length=1024)
    nutrients = models.CharField(max_length=1024)
    garden_id = models.ForeignKey(GardenBed, verbose_name='garden_id', on_delete=models.CASCADE)


class Plot(models.Model):
    #внешний ключ на id грядку, размер
    size = models.FloatField()
    garden_id = models.ForeignKey(GardenBed, verbose_name='garden_id', on_delete=models.CASCADE)


class Order(models.Model):
    #срок,внешний ключ на id грядку, внешний ключ на id растение, внешний ключ на id работник, внешний ключ на id удобрение
    deadline = models.DateField()
    garden_id = models.ForeignKey(GardenBed, verbose_name='garden_id', on_delete=models.PROTECT)
    plant_id = models.ForeignKey(Plant, verbose_name='plant_id', on_delete=models.PROTECT)
    worker_id = models.ForeignKey(Worker, verbose_name='worker_id', on_delete=models.PROTECT)
    fertilizer_id = models.ForeignKey(Fertilizer, verbose_name='fertilizer_id', on_delete=models.PROTECT)

