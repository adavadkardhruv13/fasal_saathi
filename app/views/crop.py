import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from app.models import  Crop
from app.serializers import StorageSerializer, CropSerializer
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
import csv

    
@api_view(['GET'])
def cropInfo(request, crop_name):
    if request.method == 'GET':
        crop = Crop.objects.get(name=crop_name)
        serializer = CropSerializer(crop)
        return JsonResponse(serializer.data)
    
@api_view(['GET'])
def allcrop(request):
    if request.method == 'GET':
        crop = Crop.objects.all()
        serializer = CropSerializer(crop, many=True)
        return JsonResponse(serializer.data, safe=False)