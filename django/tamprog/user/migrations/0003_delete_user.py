# Generated by Django 4.2.16 on 2024-10-26 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_person_remove_user_groups_and_more'),
        ('garden', '0009_alter_bed_rented_by_alter_field_owner'),
        ('orders', '0002_alter_order_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
