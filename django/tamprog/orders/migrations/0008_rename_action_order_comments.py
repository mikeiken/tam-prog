# Generated by Django 4.2.16 on 2024-11-22 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_total_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='action',
            new_name='comments',
        ),
    ]
