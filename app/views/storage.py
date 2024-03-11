
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from app.models import StorageSpace, Crop
from app.serializers import StorageSerializer, CropSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, date
from django.db.models import Q
from django.shortcuts import get_list_or_404

# Create your views here.


#api endpoint to get all storages
@api_view(['GET'])
def view_all_storages(request):
    if request.method == 'GET':
        storage = StorageSpace.objects.all()
        serializer = StorageSerializer(storage, many=True)
        return JsonResponse(serializer.data,safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_storage(request):
    if request.method == 'POST':
        serializer = StorageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,safe=False, status=status.HTTP_200_OK)
    else:
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#endpoint to get details of perticular storage
@api_view(['GET'])
def perticular_storage_details(request,pk):
    try:
        details = StorageSpace.objects.get(pk=pk)
    except details.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        serializer = StorageSerializer(details)
        return JsonResponse(serializer.data, safe=False)



@api_view(['GET'])
def storage_space_availability_filter(request):
    availability = request.GET.get('availability', '').lower()

    if availability == '':
        return JsonResponse({'error': 'Availability parameter is required'}, status=400)

    if availability == 'yes':
        storage_spaces = StorageSpace.objects.filter(available='Yes')
    elif availability == 'no':
        storage_spaces = StorageSpace.objects.filter(available='No')
    else:
        return JsonResponse({'error': 'Invalid value for availability parameter'}, status=400)

    serializer = StorageSerializer(storage_spaces, many=True)
    return JsonResponse(serializer.data, safe=False)



@api_view(['GET'])
def storage_space_type_filter(request):
    storage_type = request.GET.get('storage_type', '').capitalize()

    if storage_type not in ['Hot', 'Cold']:
        return JsonResponse({'error': 'Invalid value for storage_type parameter'}, status=400)

    try:
        # Case-insensitive filtering for storage_type
        storage_type = StorageSpace.objects.filter(storage_type__iexact=storage_type)
        
        serializer = StorageSerializer(storage_type, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
    
@api_view(['GET'])
def storage_space_capacity_filter(request):
    #storage_type = request.GET.get('storage_type', '').capitalize()
    min_capacity = request.GET.get('min_capacity')
    max_capacity = request.GET.get('max_capacity')
    
    try:
        #storage_space = StorageSpace.objects.filter(storage_type__iexact=storage_type)

        
        if min_capacity:
            storage_space = StorageSpace.objects.filter(capacity__gt=float(min_capacity))
        if max_capacity:
            storage_space = StorageSpace.objects.filter(capacity__lt=float(max_capacity))
            
        serializer = StorageSerializer(storage_space, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@api_view(['POST'])
def book_storage(request, id):
    try:
        storage_space = StorageSpace.objects.get(id=id)
    except StorageSpace.DoesNotExist:
        return Response({'error': 'Storage space not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        data = request.data
        quantity_to_book = int(data.get('quantity', 0))

        try:
            capacity_quantity = int(storage_space.capacity)
        except ValueError:
            return Response({'error': 'Invalid value for available quantity'}, status=status.HTTP_400_BAD_REQUEST)

        if quantity_to_book <= 0:
            return Response({'error': 'Invalid or non-positive quantity value'}, status=status.HTTP_400_BAD_REQUEST)

        if capacity_quantity >= quantity_to_book:
            storage_space.capacity = str(capacity_quantity - quantity_to_book)
            storage_space.save()
            
            if storage_space.capacity == '0':
                storage_space.delete()

            serializer = StorageSerializer(storage_space)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Not enough quantity available for booking'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def search_storage(request):
    name_query = request.GET.get('name')
    location_query = request.GET.get('location')

    if name_query:
        storages = get_list_or_404(StorageSpace, name__icontains=name_query)
    elif location_query:
        storages = get_list_or_404(StorageSpace, location__icontains=location_query)
    else:
        # Handle the case when neither name nor location is provided
        return JsonResponse({'error': 'Name or location parameter is required'}, status=400)

    serializer = StorageSerializer(storages, many=True)
    return JsonResponse(serializer.data, safe=False)