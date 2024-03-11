# Generated by Django 5.0 on 2024-03-09 06:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_remove_storagespace_booked_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storagespace',
            name='storage_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])]),
        ),
    ]
