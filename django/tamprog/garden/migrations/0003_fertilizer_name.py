# Generated by Django 4.2.16 on 2024-10-16 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0002_remove_plant_fertilizer_id_order_fertilizer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='fertilizer',
            name='name',
            field=models.CharField(default=1, max_length=1024),
            preserve_default=False,
        ),
    ]
