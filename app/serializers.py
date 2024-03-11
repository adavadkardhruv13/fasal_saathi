from rest_framework import serializers
from .models import StorageSpace, Crop

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageSpace
        fields = ['id', 'name','location', 'capacity', 'available','availability_duration','contact', 'storage_type', 'storage_image', 'price', 'available_from']
        
        
class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'