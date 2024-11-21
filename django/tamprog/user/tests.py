import pytest
from rest_framework import status
from unittest.mock import patch, MagicMock
from user.models import Worker
from user.services import WorkerService
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_register_user(api_client, register_data):
    """Тест успешной регистрации нового пользователя."""
    url = '/api/v1/register/'
    response = api_client.post(url, register_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username=register_data['username']).exists()


@pytest.mark.django_db
def test_register_user_existing_username(api_client, register_data, user):
    """Тест на регистрацию пользователя с уже существующим именем."""
    register_data['username'] = user.username
    url = '/api/v1/register/'
    response = api_client.post(url, register_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data


@pytest.mark.django_db
def test_register_user_missing_fields(api_client):
    """Тест на регистрацию без обязательных полей."""
    url = '/api/v1/register/'
    response = api_client.post(url, {}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data
    assert "phone_number" in response.data
    assert "password" in response.data


@pytest.mark.django_db
def test_register_user_invalid_phone_number(api_client, register_data):
    """Тест на регистрацию с неверным форматом номера телефона."""
    register_data['phone_number'] = 'invalid_phone'
    url = '/api/v1/register/'
    response = api_client.post(url, register_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "phone_number" in response.data


@pytest.mark.django_db
def test_login_user(api_client, user):
    """Тест успешного входа с корректными данными."""
    url = '/api/v1/login/'
    data = {'username': user.username, 'password': 'testpassword'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert 'wallet_balance' in response.data


@pytest.mark.django_db
def test_login_user_invalid_credentials(api_client):
    """Тест на вход с неверными данными."""
    url = '/api/v1/login/'
    data = {'username': 'nonexistentuser', 'password': 'wrongpassword'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.data
    assert response.data["detail"] == "Invalid credentials"


@pytest.mark.django_db
def test_login_user_missing_fields(api_client):
    """Тест на вход с отсутствующими обязательными полями."""
    url = '/api/v1/login/'
    response = api_client.post(url, {}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data
    assert "password" in response.data

@pytest.mark.django_db
@patch('user.services.get_sorted_workers_task')
@patch('user.services.AsyncResult')
def test_get_sorted_workers_ascending(mock_async_result, mock_task, workers):
    mock_task_instance = MagicMock()
    mock_task_instance.id = 'task_id'
    mock_task.delay.return_value = mock_task_instance

    mock_async_result_instance = MagicMock()
    mock_async_result_instance.get.return_value = sorted(workers, key=lambda w: w.price)
    mock_async_result.return_value = mock_async_result_instance

    sorted_workers = WorkerService.get_sorted_workers(ascending=True)
    mock_task.delay.assert_called_once_with('price', True)
    mock_async_result.assert_called_once_with('task_id')
    mock_async_result_instance.get.assert_called_once()
    assert [worker.price for worker in sorted_workers] == sorted([worker.price for worker in workers])

@pytest.mark.django_db
@patch('user.services.get_sorted_workers_task')
@patch('user.services.AsyncResult')
def test_get_sorted_workers_descending(mock_async_result, mock_task, workers):
    mock_task_instance = MagicMock()
    mock_task_instance.id = 'task_id'
    mock_task.delay.return_value = mock_task_instance

    mock_async_result_instance = MagicMock()
    mock_async_result_instance.get.return_value = sorted(workers, key=lambda w: w.price, reverse=True)
    mock_async_result.return_value = mock_async_result_instance

    sorted_workers = WorkerService.get_sorted_workers(ascending=False)
    mock_task.delay.assert_called_once_with('price', False)
    mock_async_result.assert_called_once_with('task_id')
    mock_async_result_instance.get.assert_called_once()
    assert [worker.price for worker in sorted_workers] == sorted([worker.price for worker in workers], reverse=True)


