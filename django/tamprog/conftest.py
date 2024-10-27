import pytest
from django.contrib.auth import get_user_model
from user.models import Person
from django.conf import settings
from rest_framework.test import APIClient
@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    with django_db_blocker.unblock():
        from django.test.utils import setup_databases
        setup_databases(verbosity=0, interactive=False, time_zone=settings.TIME_ZONE)

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    user = User.objects.create_user(
        username="testuser",
        password="password123",
        full_name="Test User",
        phone_number="+1234567890",
        wallet_balance=100.00
    )
    return user
