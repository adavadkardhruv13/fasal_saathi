# Generated by Django 5.0 on 2024-03-09 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_alter_storagespace_storage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='soil',
            field=models.CharField(max_length=2000),
        ),
    ]
