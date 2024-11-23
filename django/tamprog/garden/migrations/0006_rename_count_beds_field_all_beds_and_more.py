# Generated by Django 4.2.16 on 2024-11-22 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0005_alter_field_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='field',
            old_name='count_beds',
            new_name='all_beds',
        ),
        migrations.AddField(
            model_name='field',
            name='count_free_beds',
            field=models.IntegerField(default=0),
        ),
    ]
