# Generated by Django 5.0 on 2024-02-27 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_storagespace_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storagespace',
            name='available',
            field=models.CharField(max_length =6, default=False),
        ),
    ]
