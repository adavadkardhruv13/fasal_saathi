from django.db import models
from django.utils import timezone
#from django.core.validators import FileExtensionValidator
from datetime import date


# Create your models here.



AVAILABILITY_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    

class StorageSpace(models.Model):
    name = models.CharField(max_length=200, default='storage')
    location = models.CharField(max_length=100)
    capacity = models.FloatField()
    available = models.CharField(max_length=6, default=False, choices=AVAILABILITY_CHOICES)
    available_from  = models.CharField(blank=True)
    availability_duration  = models.IntegerField( default = '1', blank = True)
    contact = models.IntegerField(max_length = 14, default=0)
    storage_type = models.CharField(max_length=20, null=True, blank=True)
    storage_image = models.CharField(max_length = 1000, default='default_image_path')
    price = models.IntegerField(default = '0', blank = True)

    def __str__(self):
        return f'name - {self.name}, Loacation - {self.location}'


class Crop(models.Model):
    
    
    crop_image = models.CharField(max_length = 1000, default='default_image_path')
    season = models.CharField(max_length = 200)
    name = models.CharField(max_length = 200)
    type = models.CharField(max_length = 200)
    month_of_harvest = models.CharField(max_length = 200)
    medicines_pesticides =models.CharField(max_length = 200, blank=True)
    soil = models.CharField(max_length = 2000)
    
    def __str__(self):
        return (self.name)