# Generated by Django 4.2.16 on 2024-11-01 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_total_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='completed_at',
            field=models.DateTimeField(null=True),
        ),
    ]
