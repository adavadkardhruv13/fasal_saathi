# Generated by Django 5.0 on 2024-03-03 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_storagespace_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storagespace',
            name='available',
        ),
    ]
