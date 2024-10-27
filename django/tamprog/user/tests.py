import pytest
from django.contrib.auth import get_user_model
from .models import Person
from .services import PersonService  # Предполагается, что ваш сервис находится в файле services.py

User = get_user_model()


@pytest.mark.django_db
class TestPersonService:

    @pytest.fixture
    def person(self):
        return Person.objects.create(
            username="testuser",
            full_name="Test User",
            phone_number="+7234567890",
            wallet_balance=100
        )

    def test_update_wallet_balance(self, person):
        initial_balance = person.wallet_balance
        amount = 50.00
        updated_person = PersonService.update_wallet_balance(person_id=person.id, amount=amount)

        assert updated_person.wallet_balance == initial_balance + amount
        assert Person.objects.get(id=person.id).wallet_balance == initial_balance + amount

    def test_create_user(self):
        user_data = {
            "username": "newuser",
            "full_name": "New User",
            "phone_number": "+0987654321",
            "password": "password123",
            "wallet_balance": 150.00
        }

        user = PersonService.create_user(
            username=user_data["username"],
            full_name=user_data["full_name"],
            phone_number=user_data["phone_number"],
            password=user_data["password"],
            wallet_balance=user_data["wallet_balance"]
        )

        assert user.username == user_data["username"]
        assert user.full_name == user_data["full_name"]
        assert user.phone_number == user_data["phone_number"]
        assert user.check_password(user_data["password"]) is True
        assert user.wallet_balance == user_data["wallet_balance"]
