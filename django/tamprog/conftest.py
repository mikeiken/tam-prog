import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
User = get_user_model()

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

