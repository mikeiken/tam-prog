

import pytest
from yaml import compose

from garden.models import Agronomist, Supplier, Worker, GardenBed, Fertilizer, User, Plant, Plot, Order, AvailablePlants
from django.utils import timezone

# Тесты для модели Agronomist
@pytest.mark.django_db
def test_create_agronomist():
    agronomist = Agronomist.objects.create(
        salary=50000,
        days_work="Пн-Пт",
        work_schedule="9:00-18:00"
    )
    assert agronomist.salary == 50000
    assert agronomist.days_work == "Пн-Пт"
    assert agronomist.work_schedule == "9:00-18:00"

# Тесты для модели Supplier
@pytest.mark.django_db
def test_create_supplier():
    supplier = Supplier.objects.create(
        email="supplier@example.com",
        account_number="+79994447208"
    )
    assert supplier.email == "supplier@example.com"
    assert supplier.account_number == "+79994447208"

# Тесты для модели Worker
@pytest.mark.django_db
def test_create_worker():
    worker = Worker.objects.create(
        job_title="Рабочий",
        salary=30000,
        days_work="Пн-Ср",
        work_schedule="8:00-17:00"
    )
    assert worker.job_title == "Рабочий"
    assert worker.salary == 30000
    assert worker.days_work == "Пн-Ср"
    assert worker.work_schedule == "8:00-17:00"

# Тесты для модели GardenBed
@pytest.mark.django_db
def test_create_gardenbed():
    garden_bed = GardenBed.objects.create(
        state="Чернозем",
        size=10.5,
        price = 10
    )
    assert garden_bed.state == "Чернозем"
    assert garden_bed.size == 10.5
    assert garden_bed.price == 10

# Тесты для модели Fertilizer
@pytest.mark.django_db
def test_create_fertilizer():
    fertilizer = Fertilizer.objects.create(
        compound="Азот, Фосфор",
        price = 10,
        boost = 4,
        name = "Навоз"
    )
    assert fertilizer.compound == "Азот, Фосфор"
    assert fertilizer.price == 10
    assert fertilizer.boost == 4
    assert fertilizer.name == "Навоз"


# Тесты для модели User
@pytest.mark.django_db
def test_create_user(agronomist, worker):
    user = User.objects.create(
        password="hashed_password",
        login="user123",
        role="admin",
        email="user@example.com",
        phone="+1234567890",
        agronomist_id=agronomist,
        worker_id=worker
    )
    assert user.password == "hashed_password"
    assert user.login == "user123"
    assert user.role == "admin"
    assert user.email == "user@example.com"
    assert user.phone == "+1234567890"
    assert user.agronomist_id == agronomist
    assert user.worker_id == worker

# Тесты для модели Plant
@pytest.mark.django_db
def test_create_plant(garden_bed):
    plant = Plant.objects.create(
        name="Помидор",
        growth_time=24,
        description="Великое",
        garden_id=garden_bed,
        price=10,
        landing_data = "2024-09-03"
    )
    assert plant.name == "Помидор"
    assert plant.growth_time == 24
    assert plant.description == "Великое"
    assert plant.garden_id == garden_bed
    assert plant.price == 10
    assert plant.landing_data == "2024-09-03"

# Тесты для модели Plot
@pytest.mark.django_db
def test_create_plot(garden_bed):
    plot = Plot.objects.create(
        size=20.0,
        garden_id=garden_bed
    )
    assert plot.size == 20.0
    assert plot.garden_id == garden_bed

# Тесты для модели Order
@pytest.mark.django_db
def test_create_order(garden_bed, plant, worker, fertilizer):
    order = Order.objects.create(
        deadline=timezone.now().date(),
        garden_id=garden_bed,
        plant_id=plant,
        worker_id=worker,
        fertilizer_id=fertilizer
    )
    assert order.deadline == timezone.now().date()
    assert order.garden_id == garden_bed
    assert order.plant_id == plant
    assert order.worker_id == worker
    assert order.fertilizer_id == fertilizer


@pytest.mark.django_db
def test_create_available_plant():
    plant = AvailablePlants.objects.create(
        name="Помидор",
        price=15.5,
        growth_time=90,
        description="Красный сочный овощ",
        landing_data="2024-05-10",
        garden_id=1
    )

    assert plant.name == "Помидор"
    assert plant.price == 15.5
    assert plant.growth_time == 90
    assert plant.description == "Красный сочный овощ"
    assert str(plant.landing_data) == "2024-05-10"
    assert plant.garden_id == 1
