# Generated by Django 4.2.16 on 2024-11-26 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_rename_action_order_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comments',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
