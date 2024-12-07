import pytest
from garden.models import Field, Bed
from fertilizer.models import Fertilizer, BedPlant, BedPlantFertilizer
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

@pytest.fixture
def celery_settings(settings):
    """Настройка тестового окружения для Celery"""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

@pytest.fixture
def api_client():
    return APIClient()

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
    # Создаем 5 участков, каждый из которых имеет уникальное имя и цену
    return mixer.cycle(5).blend('garden.Field',
                                name=lambda: mixer.faker.city(),
                                price=lambda: mixer.faker.random_number(digits=3) * 1.0,
                                count_beds=10)

@pytest.fixture
def beds(fields, person):
    # Создаем 10 грядок, которые могут быть арендованы или не арендованы
    # Для арендованных грядок будет назначен пользователь как арендатор
    return mixer.cycle(10).blend(
        'garden.Bed',
        field=lambda: mixer.faker.random_element(fields),  # связываем грядки с участками
        is_rented=lambda: mixer.faker.boolean(),  # случайным образом определяем арендуемая ли грядка
        rented_by=lambda: person if mixer.faker.boolean() else None  # если арендована, назначаем арендатора
    )

@pytest.fixture
def fertilizers():
    # Создаем несколько удобрений с уникальными составами
    return mixer.cycle(5).blend('fertilizer.Fertilizer',
                                name=lambda: f"Fertilizer {mixer.faker.word()}",
                                boost=lambda: mixer.faker.random_int(min=1, max=10),
                                compound=lambda: mixer.faker.sentence(nb_words=3))

@pytest.fixture
def plants():
    # Создаем 10 растений с уникальными именами, описанием и стоимостью
    return mixer.cycle(10).blend('plants.Plant',
                                 name=lambda: mixer.faker.word(),
                                 growth_time=lambda: mixer.faker.random_int(min=5, max=30),
                                 price=lambda: mixer.faker.random_number(digits=2) * 1.0,
                                 description=lambda: mixer.faker.text(max_nb_chars=100))

@pytest.fixture
def bed_plants(beds, plants):
    # Создаем посадки растений на грядках
    bed_plants = mixer.cycle(10).blend('plants.BedPlant',
                                       bed=lambda: mixer.faker.random_element(beds),
                                       plant=lambda: mixer.faker.random_element(plants),
                                       fertilizer_applied=mixer.faker.boolean(),
                                       growth_time=lambda: mixer.faker.random_int(min=5, max=30))
    return bed_plants

@pytest.fixture
def bed_plant_fertilizers(bed_plants, fertilizers):
    # Применяем удобрения к посадкам
    bed_plant_fertilizers = mixer.cycle(10).blend('fertilizer.BedPlantFertilizer',
                                                  bed_plant=lambda: mixer.faker.random_element(bed_plants),
                                                  fertilizer=lambda: mixer.faker.random_element(fertilizers))
    return bed_plant_fertilizers


@pytest.fixture
def workers():
    # Создаем 10 рабочих с уникальными именами и стоимостью услуг
    return mixer.cycle(10).blend('user.Worker',
                                 name=lambda: mixer.faker.name(),
                                 price=lambda: mixer.faker.random_number(digits=2) * 1.0,
                                 description=lambda: mixer.faker.text(max_nb_chars=100))

@pytest.fixture
def orders(user, workers, beds, plants):
    # Создаем 10 заказов для пользователя, связанных с рабочими, грядками и растениями
    return mixer.cycle(10).blend('orders.Order',
                                 user=user,
                                 worker=lambda: mixer.faker.random_element(workers),
                                 bed=lambda: mixer.faker.random_element(beds),
                                 plant=lambda: mixer.faker.random_element(plants),
                                 action=lambda: mixer.faker.word(),
                                 completed_at=lambda: None if mixer.faker.boolean() else timezone.now(),
                                 total_cost=lambda: mixer.faker.random_number(digits=3) * 1.0)

