import pytest
from garden.models import Field, Bed
from fertilizer.models import Fertilizer, BedPlant, BedPlantFertilizer
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def fertilizer():
    return mixer.blend(Fertilizer, name="NPK", boost=5, compound="Nitrogen-Phosphorus-Potassium")

@pytest.fixture
def bed_plant():
    return mixer.blend(BedPlant)

@pytest.fixture
def bed_plant_fertilizer(bed_plant, fertilizer):
    return mixer.blend(BedPlantFertilizer, bed_plant=bed_plant, fertilizer=fertilizer)

@pytest.fixture
def user():
    user = mixer.blend(User, username='testuser')
    user.set_password('testpassword')
    user.save()
    return user

@pytest.fixture
def person():
    return mixer.blend('user.Person')

@pytest.fixture
def fields():
    return mixer.cycle(5).blend('garden.Field', price=mixer.faker.random_number(digits=3) * 1.0)

@pytest.fixture
def beds():
    return mixer.cycle(5).blend('garden.Bed', is_rented=mixer.faker.boolean())

@pytest.fixture
def orders(user):
    incomplete_orders = mixer.cycle(5).blend('orders.Order', user=user, completed_at=None)
    completed_orders = mixer.cycle(5).blend('orders.Order', user=user,
        completed_at=mixer.faker.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone()))
    return incomplete_orders + completed_orders

@pytest.fixture
def plants():
    return mixer.cycle(10).blend('plants.Plant', name=mixer.faker.word())

@pytest.fixture
def bed_plants(user, beds, plants):
    return mixer.cycle(5).blend(
        'plants.BedPlant',
        plant=mixer.faker.random_element(plants),
        bed=mixer.faker.random_element(beds)
    )

@pytest.fixture
def workers():
    return mixer.cycle(10).blend('user.Worker', name=mixer.faker.name())

@pytest.fixture
def field():
    return mixer.blend(Field, count_beds=5)

@pytest.fixture
def bed(field, person):
    return mixer.blend(Bed, field=field, is_rented=False, rented_by=None)

from mixer.backend.django import mixer
from user.models import Person
from orders.models import Worker, Bed, Plant, Order

@pytest.fixture
def user1():
    return mixer.blend(Person, wallet_balance=1000)

@pytest.fixture
def worker():
    return mixer.blend(Worker, price=100)

@pytest.fixture
def bed1():
    return mixer.blend(Bed, field__price=200)

@pytest.fixture
def plant():
    return mixer.blend(Plant, price=150)

@pytest.fixture
def order(user, worker, bed, plant):
    return mixer.blend(Order, user=user, worker=worker, bed=bed, plant=plant)
