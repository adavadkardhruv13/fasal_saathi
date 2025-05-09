from django.db import models
from django.utils import timezone
#from django.core.validators import FileExtensionValidator
from datetime import date
from django.contrib.auth.models import User


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
    storage_image = models.ImageField(max_length = 1000, default='default_image_path')
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
    
    
class HarvestListing(models.Model):
    LISTING_STATUS = [
        ('available', 'Available'),
        ('pending', 'Sale Pending'),
        ('sold', 'Sold')
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='harvest_listings')
    crop_type = models.ForeignKey('Crop', on_delete=models.CASCADE )
    title = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    harvest_date = models.DateField
    listing_date = models.DateField(default=date.today)
    loaction = models.CharField(max_length=200)
    quality_grade = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=LISTING_STATUS, default='available')
    organic_certified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.titel} - {self.quantity}{self.unit} ({self.status})"
    
    
class Equipment(models.Model):
    EQUIPMENT_CATEGORIES = [
        ('tractor', 'Tractor'),
        ('harvester', 'Harvester'),
        ('plow', 'Plow'),
        ('seeder', 'Seeder'),
        ('sprayer', 'Sprayer'),
        ('irrigation', 'Irrigation Equipment'),
        ('other', 'Other')
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='harvest_listings')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=EQUIPMENT_CATEGORIES)
    description = models.TextField()
    manufacturer = models.CharField(max_length=200, blank=True)
    model = models.CharField(max_length=200, blank=True)
    manufacturing_year = models.PositiveSmallIntegerField(blank=True, null=True)
    equipment_image = models.CharField(max_length=1000, default='default_equipment_image')
    
    def __str__(self):
        return f"{self.name} ({self.category})"
    
class EquipmentRental(models.Model):
    RENTAL_STATUS = [
        ('available', 'Available'),
        ('rented', 'Currently Rented'),
        ('maintenance', 'Under Maintenance'),
        ('unavailable', 'Unavailable')
    ]
    
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='rentals')
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_rental_days = models.PositiveSmallIntegerField(default=1)
    location = models.CharField(max_length=200)
    available_from = models.DateField()
    available_until = models.DateField(blank=True, null=True)
    operator_included = models.BooleanField(default=False)
    delivery_available = models.BooleanField(default=False)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=RENTAL_STATUS, default='available')
    
    def __str__(self):
        return f"{self.equipment.name} - ₹{self.daily_rate}/day ({self.status})"

class RentalBooking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending Approval'),
        ('confirmed', 'Confirmed'),
        ('active', 'Currently Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    rental = models.ForeignKey(EquipmentRental, on_delete=models.CASCADE, related_name='bookings')
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipment_bookings')
    # renter = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_location = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Booking for {self.rental.equipment.name} ({self.start_date} to {self.end_date})"

class HarvestPurchase(models.Model):
    PURCHASE_STATUS = [
        ('pending', 'Pending'),
        ('payment_received', 'Payment Received'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    listing = models.ForeignKey(HarvestListing, on_delete=models.CASCADE, related_name='purchases')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='harvest_purchases')
    # buyer = models.CharField(max_length=200)
    quantity = models.FloatField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PURCHASE_STATUS, default='pending')
    delivery_address = models.CharField(max_length=200, blank=True, null=True)
    pickup_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Purchase from {self.listing.title} by {self.buyer.username}"
    