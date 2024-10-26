import pytest
from garden.serializers import *
from django.utils import timezone
# Тест для сериализатора Agronomist
@pytest.mark.django_db
def test_agronomist_serializer():
    data = {
        "salary": 50000,
        "days_work": "Пн-Пт",
        "work_schedule": "9:00-18:00"
    }
    serializer = AgronomistSerializer(data=data)
    assert serializer.is_valid()
    agronomist = serializer.save()
    assert agronomist.salary == 50000
    assert agronomist.days_work == "Пн-Пт"
    assert agronomist.work_schedule == "9:00-18:00"

# Тест для сериализатора Supplier
@pytest.mark.django_db
def test_supplier_serializer():
    data = {
        "email": "supplier@example.com",
        "account_number": "123456789"
    }
    serializer = SupplierSerializer(data=data)
    assert serializer.is_valid()
    supplier = serializer.save()
    assert supplier.email == "supplier@example.com"
    assert supplier.account_number == "123456789"

# Тест для сериализатора Worker
@pytest.mark.django_db
def test_worker_serializer():
    data = {
        "job_title": "Рабочий",
        "salary": 30000,
        "days_work": "Пн-Ср",
        "work_schedule": "8:00-17:00"
    }
    serializer = WorkerSerializer(data=data)
    assert serializer.is_valid()
    worker = serializer.save()
    assert worker.job_title == "Рабочий"
    assert worker.salary == 30000
    assert worker.days_work == "Пн-Ср"
    assert worker.work_schedule == "8:00-17:00"

# Тест для сериализатора GardenBed
@pytest.mark.django_db
def test_garden_bed_serializer():
    data = {
        "state": "Хорошее",
        "size": 10.5,
        "price": 10
    }
    serializer = GardenBedSerializer(data=data)
    assert serializer.is_valid()
    garden_bed = serializer.save()
    assert garden_bed.state == "Хорошее"
    assert garden_bed.size == 10.5
    assert garden_bed.price == 10

# Тест для сериализатора Fertilizer
@pytest.mark.django_db
def test_fertilizer_serializer():
    data = {
        "compound": "Азот, Фосфор",
        "price": 10,
        "boost" : 4,
        "name" : "Навоз"
    }
    serializer = FertilizerSerializer(data=data)
    assert serializer.is_valid()
    fertilizer = serializer.save()
    assert fertilizer.compound == "Азот, Фосфор"
    assert fertilizer.price == 10
    assert fertilizer.boost == 4
    assert fertilizer.name == "Навоз"

# Тест для сериализатора User
@pytest.mark.django_db
def test_user_serializer(agronomist, worker):
    data = {
        "password": "hashed_password",
        "login": "user123",
        "role": "admin",
        "email": "user@mail.ru",
        "phone": "+72345678908",
        "agronomist_id": agronomist.id,
        "worker_id": worker.id
    }
    serializer = UserSerializer(data=data)
    assert serializer.is_valid(), serializer.errors  # Добавлено для отладки
    user = serializer.save()
    assert user.password == "hashed_password"
    assert user.login == "user123"
    assert user.role == "admin"
    assert user.email == "user@mail.ru"
    assert user.phone == "+72345678908"
    assert user.agronomist_id == agronomist
    assert user.worker_id == worker

@pytest.mark.django_db
def test_plant_serializer(garden_bed):
    data = {
        "name": "Помидор",
        "growth_time": 24,
        "description": "Великое",
        "garden_id": garden_bed.id,
        "price": 10,
        "landing_data": timezone.now().date().isoformat()

    }

    serializer = PlantSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    plant = serializer.save()


    assert plant.name == "Помидор"
    assert plant.growth_time == 24
    assert plant.description == "Великое"
    assert plant.garden_id == garden_bed
    assert plant.price == 10
    assert plant.landing_data == timezone.now().date()


# Тест для сериализатора Plot
@pytest.mark.django_db
def test_plot_serializer(garden_bed):
    data = {
        "size": 20.0,
        "garden_id": garden_bed.id
    }
    serializer = PlotSerializer(data=data)
    assert serializer.is_valid()
    plot = serializer.save()
    assert plot.size == 20.0
    assert plot.garden_id == garden_bed

# Тест для сериализатора Order
@pytest.mark.django_db
def test_order_serializer(garden_bed, plant, worker, fertilizer):
    data = {
        "deadline": timezone.now().date(),
        "garden_id": garden_bed.id,
        "plant_id": plant.id,
        "worker_id": worker.id,
        "fertilizer_id": fertilizer.id
    }
    serializer = OrderSerializer(data=data)
    assert serializer.is_valid()
    order = serializer.save()
    assert order.deadline == timezone.now().date()
    assert order.garden_id == garden_bed
    assert order.plant_id == plant
    assert order.worker_id == worker
    assert order.fertilizer_id == fertilizer
