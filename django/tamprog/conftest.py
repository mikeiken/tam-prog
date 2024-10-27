from user.services import Person
import pytest
@pytest.fixture
def person(db):
    user = Person.objects.create(
        username='testuser',
        full_name='Test User',
        phone_number='+1234567890',
        wallet_balance=100.00
    )
    return user