import pytest
from garden.models import Agronomist, Supplier, Worker, GardenBed, Fertilizer, User, Plant, Plot, Order
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
    return GardenBed.objects.create(state="Хорошее", size=10.5)

@pytest.fixture
def fertilizer():
    return Fertilizer.objects.create(compound="Азот, Фосфор")

@pytest.fixture
def user(agronomist, worker):
    return User.objects.create(password="hashed_password", login="user123", role="admin",
                               email="user@example.com", phone="+1234567890",
                               agronomist_id=agronomist, worker_id=worker)

@pytest.fixture
def plant(garden_bed):
    return Plant.objects.create(name="Помидор", growth_conditions="Тепло, Влажно",
                                 nutrients="Азот, Калий", garden_id=garden_bed)

@pytest.fixture
def plot(garden_bed):
    return Plot.objects.create(size=20.0, garden_id=garden_bed)

@pytest.fixture
def order(garden_bed, plant, worker, fertilizer):
    return Order.objects.create(deadline="2024-10-19", garden_id=garden_bed,
                                 plant_id=plant, worker_id=worker, fertilizer_id=fertilizer)
