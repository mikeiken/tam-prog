# Generated by Django 4.2.16 on 2024-09-28 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='fertilizer_id',
        ),
        migrations.AddField(
            model_name='order',
            name='fertilizer_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='garden.fertilizer', verbose_name='fertilizer_id'),
            preserve_default=False,
        ),
    ]
