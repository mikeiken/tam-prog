from .models import Person, Agronomist, Worker


class PersonService:
    @staticmethod
    def update_wallet_balance(person_id, amount):
        person = Person.objects.get(id=person_id)
        person.wallet_balance += amount
        person.save()
        return person
