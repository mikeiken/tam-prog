import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.conf import settings
from django.contrib.auth import get_user_model
from logging import getLogger

log = getLogger(__name__)

class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Store original REQUIRED_FIELDS
        original_required = User.REQUIRED_FIELDS

        try:
            User.REQUIRED_FIELDS = []

            username = settings.DJANGO_SUPER_USER
            password = settings.DJANGO_SUPER_PASSWORD

            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING('Superuser already exists'))
                log.info(f"Superuser {username} already exists")
                return

            user = User._default_manager.create(
                username=username,
                is_staff=True,
                is_superuser=True,
            )
            user.set_password(password)
            user.save()
            # User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
            log.info(f"Superuser {username} created successfully")
        except AttributeError as e:
            self.stdout.write(self.style.ERROR('Missing required settings. Please check DJANGO_SUPER_USER, DJANGO_SUPER_EMAIL, and DJANGO_SUPER_PASSWORD in settings.py'))
            log.error(f"Missing required settings. Please check DJANGO_SUPER_USER, DJANGO_SUPER_EMAIL, and DJANGO_SUPER_PASSWORD in settings.py")
            log.exception(e)
        finally:
            User.REQUIRED_FIELDS = original_required