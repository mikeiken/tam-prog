from .models import Person, Agronomist, Worker
from django.contrib.auth import get_user_model
User = get_user_model()

class PersonService:
    @staticmethod
    def update_wallet_balance(person_id, amount):
        person = Person.objects.get(id=person_id)
        person.wallet_balance += amount
        person.save()
        return person

    @staticmethod
    def create_user(username, full_name, phone_number, password, wallet_balance=0.00):
        user = User.objects.create_user(
            username=username,
            full_name=full_name,
            phone_number=phone_number,
            password=password,
            wallet_balance=wallet_balance
        )
        return user