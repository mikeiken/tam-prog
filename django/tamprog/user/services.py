from .models import User, Agronomist
from rest_framework_simplejwt.tokens import RefreshToken

def create_user(username, password, wallet_balance=0.00, phone_number='', account_number='', full_name='', role='user'):
    user = User.objects.create_user(
        username=username,
        password=password,
        wallet_balance=wallet_balance,
        phone_number=phone_number,
        account_number=account_number,
        full_name=full_name,
        role=role
    )
    return user

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def update_user(user, phone_number=None, account_number=None, full_name=None):
    if phone_number is not None:
        user.phone_number = phone_number
    if account_number is not None:
        user.account_number = account_number
    if full_name is not None:
        user.full_name = full_name
    user.save()
    return user
