# Generated by Django 5.0 on 2024-03-01 15:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_storagespace_storage_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='storagespace',
            name='storage_image',
            field=models.ImageField(blank=True, upload_to='images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])]),
        ),
    ]