# Generated by Django 4.2.16 on 2024-10-31 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
            preserve_default=False,
        ),
    ]
