# Generated by Django 5.0 on 2024-03-09 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_storagespace_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storagespace',
            name='contact',
            field=models.IntegerField(default=0, max_length=14),
        ),
    ]
