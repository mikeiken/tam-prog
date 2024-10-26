# Generated by Django 4.2.16 on 2024-10-26 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chel', '0001_initial'),
        ('plants', '0001_initial'),
        ('garden', '0008_bed_field_delete_availableplants_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('bed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.bed')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plants.plant')),
                ('chel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chel.chel')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chel.worker')),
            ],
        ),
    ]
