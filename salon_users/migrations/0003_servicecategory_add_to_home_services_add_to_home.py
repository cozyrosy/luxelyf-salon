# Generated by Django 5.1.4 on 2025-01-15 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon_users', '0002_servicecategory_services_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicecategory',
            name='add_to_home',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='services',
            name='add_to_home',
            field=models.BooleanField(default=False),
        ),
    ]
