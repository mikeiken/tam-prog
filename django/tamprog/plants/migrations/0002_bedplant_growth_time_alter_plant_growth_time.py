# Generated by Django 4.2.16 on 2024-10-30 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bedplant',
            name='growth_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='plant',
            name='growth_time',
            field=models.IntegerField(default=0),
        ),
    ]
