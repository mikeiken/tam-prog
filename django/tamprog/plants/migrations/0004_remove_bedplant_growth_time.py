# Generated by Django 4.2.16 on 2024-10-31 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0003_alter_bedplant_growth_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bedplant',
            name='growth_time',
        ),
    ]
