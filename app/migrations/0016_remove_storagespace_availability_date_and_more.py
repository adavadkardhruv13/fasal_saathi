# Generated by Django 5.0 on 2024-03-02 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_storagespace_availability_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storagespace',
            name='availability_date',
        ),
        migrations.AlterField(
            model_name='storagespace',
            name='name',
            field=models.CharField(default='storage', max_length=200),
        ),
    ]
