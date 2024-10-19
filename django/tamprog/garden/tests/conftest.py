import pytest
from garden.models import Agronomist, Supplier, Worker, GardenBed, Fertilizer, User, Plant, Plot, Order, AvailablePlants
from django.utils import timezone

@pytest.fixture
def agronomist():
    return Agronomist.objects.create(salary=50000, days_work="Пн-Пт", work_schedule="9:00-18:00")

@pytest.fixture
def supplier():
    return Supplier.objects.create(email="supplier@example.com", account_number="123456789")

@pytest.fixture
def worker():
    return Worker.objects.create(job_title="Рабочий", salary=30000, days_work="Пн-Ср", work_schedule="8:00-17:00")

@pytest.fixture
def garden_bed():
    return GardenBed.objects.create(state="Хорошее", size=10.5, price=10)

@pytest.fixture
def fertilizer():
    return Fertilizer.objects.create(compound="Азот, Фосфор",price = 10,
        boost = 4,
        name = "Навоз")

@pytest.fixture
def user(agronomist, worker):
    return User.objects.create(password="hashed_password", login="user123", role="admin",
                               email="user@mail.ru", phone="+72345678908",
                               agronomist_id=agronomist, worker_id=worker)

@pytest.fixture
def plant(garden_bed):
    return Plant.objects.create(name="Помидор",
        growth_time=24,
        description="Великое",
        garden_id=garden_bed,
        price=10,
        landing_data = "2024-09-03")

@pytest.fixture
def plot(garden_bed):
    return Plot.objects.create(size=20.0, garden_id=garden_bed)

@pytest.fixture
def order(garden_bed, plant, worker, fertilizer):
    return Order.objects.create(deadline="2024-10-19", garden_id=garden_bed,
                                 plant_id=plant, worker_id=worker, fertilizer_id=fertilizer)

@pytest.fixture
def available_plants(garden_bed):
    return AvailablePlants.objects.create(
        name="Помидор",
        price=15.5,
        growth_time=90,
        description="Красный сочный овощ",
        landing_data="2024-05-10",
        garden_id=1
    )