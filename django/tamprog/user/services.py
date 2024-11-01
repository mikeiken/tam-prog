from django.contrib.auth import get_user_model

User = get_user_model()

class PersonService:
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

    @staticmethod
    def update_wallet_balance(user, amount):
        if user.wallet_balance is not None and user.wallet_balance >= amount:
            user.wallet_balance -= amount
            user.save(update_fields=['wallet_balance'])
            return True
        return False

