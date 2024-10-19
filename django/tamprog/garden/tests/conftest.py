import pytest
from garden.models import Agronomist, Supplier, Worker, GardenBed, Fertilizer, User, Plant, Plot, Order
from django.utils import timezone
@pytest.fixture
def agronomist(db):
    return Agronomist.objects.create(
        salary=50000,
        days_work="Пн-Пт",
        work_schedule="9:00-18:00"
    )

@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        email="supplier@example.com",
        account_number="+79994447208"
    )

@pytest.fixture
def worker(db):
    return Worker.objects.create(
        job_title="Рабочий",
        salary=30000,
        days_work="Пн-Ср",
        work_schedule="8:00-17:00"
    )

@pytest.fixture
def garden_bed(db):
    return GardenBed.objects.create(
        state="Чернозем",
        size=10.5
    )

@pytest.fixture
def fertilizer(db):
    return Fertilizer.objects.create(
        compound="Азот, Фосфор"
    )

@pytest.fixture
def user(db, agronomist, worker):
    return User.objects.create(
        password="hashed_password",
        login="user123",
        role="admin",
        email="user@example.com",
        phone="+1234567890",
        agronomist_id=agronomist,
        worker_id=worker
    )

@pytest.fixture
def plant(db, garden_bed):
    return Plant.objects.create(
        name="Помидор",
        growth_conditions="Тепло, Влажно",
        nutrients="Азот, Калий",
        garden_id=garden_bed
    )

@pytest.fixture
def plot(db, garden_bed):
    return Plot.objects.create(
        size=20.0,
        garden_id=garden_bed
    )

@pytest.fixture
def order(db, garden_bed, plant, worker, fertilizer):
    return Order.objects.create(
        deadline=timezone.now().date(),
        garden_id=garden_bed,
        plant_id=plant,
        worker_id=worker,
        fertilizer_id=fertilizer
    )
