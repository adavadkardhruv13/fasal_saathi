from rest_framework import serializers
from .models import StorageSpace, Crop, HarvestListing, HarvestPurchase, Equipment, EquipmentRental, RentalBooking
from django.contrib.auth.models import User

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageSpace
        fields = ['id', 'name','location', 'capacity', 'available','availability_duration','contact', 'storage_type', 'storage_image', 'price', 'available_from']
        
        
class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'
        
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class HarvestListingSerializer(serializers.ModelSerializer):
    owner_details = UserSerializer(source='owner', read_only=True)
    crop_name = serializers.CharField(source='crop_type.name', read_only=True)
    
    class Meta:
        model = HarvestListing
        fields = '__all__'
        extra_fields = ['owner_details', 'crop_name']

class EquipmentSerializer(serializers.ModelSerializer):
    owner_details = UserSerializer(source='owner', read_only=True)
    
    class Meta:
        model = Equipment
        fields = '__all__'
        extra_fields = ['owner_details']

class EquipmentRentalSerializer(serializers.ModelSerializer):
    equipment_details = EquipmentSerializer(source='equipment', read_only=True)
    
    class Meta:
        model = EquipmentRental
        fields = '__all__'
        extra_fields = ['equipment_details']

class RentalBookingSerializer(serializers.ModelSerializer):
    rental_details = EquipmentRentalSerializer(source='rental', read_only=True)
    renter_details = UserSerializer(source='renter', read_only=True)
    
    class Meta:
        model = RentalBooking
        fields = '__all__'
        extra_fields = ['rental_details', 'renter_details']

class HarvestPurchaseSerializer(serializers.ModelSerializer):
    listing_details = HarvestListingSerializer(source='listing', read_only=True)
    buyer_details = UserSerializer(source='buyer', read_only=True)
    
    class Meta:
        model = HarvestPurchase
        fields = '__all__'
        extra_fields = ['listing_details', 'buyer_details']
    