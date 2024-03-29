# Generated by Django 5.0 on 2024-02-27 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StorageSpace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('capacity', models.FloatField()),
                ('available', models.FloatField()),
                ('is_shared', models.BooleanField(default=False)),
            ],
        ),
    ]
