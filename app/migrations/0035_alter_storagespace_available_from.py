# Generated by Django 5.0 on 2024-03-09 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_alter_storagespace_available_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storagespace',
            name='available_from',
            field=models.CharField(blank=True),
        ),
    ]
