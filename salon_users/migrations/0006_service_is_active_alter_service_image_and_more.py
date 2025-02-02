# Generated by Django 5.1.4 on 2025-01-23 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon_users', '0005_service_remove_userprofile_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='image',
            field=models.ImageField(upload_to='static/services/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/profiles/'),
        ),
    ]
