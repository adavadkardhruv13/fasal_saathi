# Generated by Django 5.0 on 2024-03-11 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_alter_crop_crop_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storagespace',
            name='storage_image',
        ),
        migrations.AddField(
            model_name='storagespace',
            name='crop_image',
            field=models.CharField(default='default_image_path', max_length=1000),
        ),
        migrations.AlterField(
            model_name='crop',
            name='crop_image',
            field=models.CharField(default='default_image_path', max_length=1000),
        ),
    ]
