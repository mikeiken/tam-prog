import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from user.models import Person

User = get_user_model()


@pytest.mark.django_db
def test_login_user(api_client, create_user):
    """Тестирует вход пользователя в систему."""
    url = reverse('login')  # Убедитесь, что ваш URL имеет правильное имя
    data = {
        "username": "testuser",
        "password": "password123"
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert "refresh" in response.data
    assert "access" in response.data
    assert response.data["wallet_balance"] == create_user.wallet_balance




@pytest.mark.django_db
def test_get_person(api_client, create_user):
    """Тестирует получение информации о человеке."""
    person = Person.objects.create(
        username="personuser",
        full_name="Person User",
        phone_number="+1112223333",
        wallet_balance=200.00
    )

    url = reverse('person-detail', kwargs={'pk': person.id})  # Убедитесь, что ваш URL имеет правильное имя
    api_client.login(username="testuser", password="password123")  # Логин пользователя

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == person.username
    assert response.data['full_name'] == person.full_name

@pytest.mark.django_db
def test_update_person(api_client, create_user):
    person = Person.objects.create(
        username="personuser",
        full_name="Person User",
        phone_number="+1112223333",
        wallet_balance=200.00
    )

    url = reverse('person-detail', kwargs={'pk': person.id})  # Убедитесь, что ваш URL имеет правильное имя
    api_client.login(username="testuser", password="password123")  # Логин пользователя

    data = {
        "full_name": "Updated Person User",
        "phone_number": "+9998887777"
    }

    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    person.refresh_from_db()  # Обновление объекта из базы данных
    assert person.full_name == "Updated Person User"

