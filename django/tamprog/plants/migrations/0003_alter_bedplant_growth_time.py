# Generated by Django 4.2.16 on 2024-10-31 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0002_bedplant_growth_time_alter_plant_growth_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bedplant',
            name='growth_time',
            field=models.IntegerField(),
        ),
    ]