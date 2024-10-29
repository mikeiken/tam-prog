import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_register_user(api_client):
    """Тест успешной регистрации нового пользователя."""
    url = '/api/v1/register/'
    data = {
        'username': 'newuser',
        'phone_number': '+1234567890',
        'full_name': 'New User',
        'password': 'newpassword',
        'wallet_balance': 100.00
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_register_user_existing_username(api_client, user):
    """Тест на регистрацию пользователя с уже существующим именем."""
    url = '/api/v1/register/'
    data = {
        'username': user.username,
        'phone_number': '+1234567890',
        'full_name': 'New User',
        'password': 'newpassword',
        'wallet_balance': 50.00
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data

@pytest.mark.django_db
def test_register_user_missing_fields(api_client):
    """Тест на регистрацию без обязательных полей."""
    url = '/api/v1/register/'
    data = {
        'username': 'incompleteuser'
        # Пропущены обязательные поля
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "phone_number" in response.data
    assert "password" in response.data

@pytest.mark.django_db
def test_register_user_invalid_phone_number(api_client):
    """Тест на регистрацию с неверным форматом номера телефона."""
    url = '/api/v1/register/'
    data = {
        'username': 'user_invalid_phone',
        'phone_number': 'invalid_phone',
        'full_name': 'New User',
        'password': 'newpassword',
        'wallet_balance': 100.00
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "phone_number" in response.data

@pytest.mark.django_db
def test_login_user(api_client, user):
    """Тест успешного входа с корректными данными."""
    user.set_password('testpassword')
    user.save()
    url = '/api/v1/login/'
    data = {
        'username': user.username,
        'password': 'testpassword'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert 'wallet_balance' in response.data

@pytest.mark.django_db
def test_login_user_invalid_credentials(api_client):
    """Тест на вход с неверными данными."""
    url = '/api/v1/login/'
    data = {
        'username': 'nonexistentuser',
        'password': 'wrongpassword'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.data
    assert response.data["detail"] == "Invalid credentials"

@pytest.mark.django_db
def test_login_user_missing_fields(api_client):
    """Тест на вход с отсутствующими обязательными полями."""
    url = '/api/v1/login/'
    data = {
        'username': 'testuser'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data
