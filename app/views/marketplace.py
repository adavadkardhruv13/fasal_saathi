from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from app.models import HarvestListing, HarvestPurchase, Equipment, EquipmentRental, RentalBooking, Crop
from app.serializers import (
    HarvestListingSerializer, EquipmentSerializer, EquipmentRentalSerializer,
    RentalBookingSerializer, HarvestPurchaseSerializer
)
from datetime import date, timedelta
from django.db.models import Q

@api_view(['GET'])
def all_harvest_listing(request):
    """Get all active harvest listing"""
    
    listing = HarvestListing.objects.filter(status='available')
    serializer = HarvestListingSerializer(listing, many=True)
    return Response(serializer.data)

@api_view({"GET", "POST"})
@permission_classes([IsAuthenticated])
def farmer_harvest_listing(request):
    """Get all listings by the logged-in farmer or create a new listing"""
    
    if request.method == 'GET':
        listing  = HarvestListing.objects.filter(owner = request.user)
        serializer = HarvestListingSerializer(listing, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()
        data['owner'] = request.user.id
        
        #handel crop type by name
        crop_name = data.get('crop_name')
        if crop_name:
            try:
                crop = Crop.objects.get(name = crop_name)
                data['crop_type'] = crop.id
            except Crop.DoesNotExist:
                return Response({'error': f'Crop "{crop_name}" not found'}, status=status.HTTP_400_BAD_REQUEST)
            
            
        serializer = HarvestListingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def harvest_lisiting_details(request, pk):
    """Retrieve, update or delete a harvest listing"""
    try:
        listing = HarvestListing.objects.get(pk=pk)
    except HarvestListing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    if request.method in ['PUT', 'DELETE'] and listing.owner != request.user:
        return Response({"error": "You don't have permission to modify this listing"}, 
                        status=status.HTTP_403_FORBIDDEN)
        
    
    if request.method == 'GET':
        serializer = HarvestListingSerializer(listing)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = request.data.copy()
        
        #handle crop by its name if provided
        crop_name = data.get('crop_name')
        if crop_name:
            try:
                crop = Crop.object.get(name = crop_name)
                data['crop_name'] = crop.id
            except Crop.DoesNotExist:
                return Response({'error': f'Crop "{crop_name}" not found'}, 
                                status=status.HTTP_400_BAD_REQUEST)
                
        serializer = HarvestListingSerializer(listing, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        listing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_harvest(request, listing_id):
    """Create purchase request for a harvest listing"""
    
    try:
        listing = HarvestListing.objects.get(pk=listing_id, status = 'available')
    except HarvestListing.DoesNotExist:
        return Response({"error": "Listing not found or not available"}, 
                        status=status.HTTP_404_NOT_FOUND)
        
    
    if listing.owner == request.user:
        return Response({"error": "You cannot purchase your own listing"}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
    data = request.data.copy()
    quantity = float(data.get('quantity',0))
    
    if quantity<=0:
        return Response({"error": "Quantity must be greater than zero"}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
    if quantity>listing.quantity:
        return Response({"error": "Requested quantity exceeds available quantity"}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
        
    total_price = quantity * float(listing.price_per_unit)
    
    purchase_data = {
        'listing': listing.id,
        'buyer': request.user.id,
        'quantity': quantity,
        'total_price': total_price,
        'delivery_address': data.get('delivery_address'),
        'pickup_date': data.get('pickup_date'),
        'notes': data.get('notes', '')
    }
    
    serializer = HarvestPurchaseSerializer(data=purchase_data)
    if serializer.is_valid():
        purchase = serializer.save()
        
        listing.quantity -= quantity
        if listing.quantity == 0:
            listing.status = 'sold'
        else:
            listing.status = 'pending'  # Mark as pending until transaction completes
        listing.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_harvest_purchase(request):
    """Get all harvest purchases made by the current user"""
    purchase = HarvestPurchase.objects.filter(buyer = request.user)
    serializer = HarvestPurchaseSerializer(purchase, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_harvest_sales(request):
    """Get all the harvest sale"""
    sale = HarvestPurchase.objects.filter(listing__owner=request.user)
    serializer = HarvestPurchaseSerializer(sale, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_purchase_status(request, purchase_id):
    """Update the status of a purchase (for both buyer and seller)"""
    try:
        purchase = HarvestPurchase.objects.get(pk=purchase_id)
    except HarvestPurchase.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Verify user is either buyer or seller
    if request.user != purchase.buyer and request.user != purchase.listing.owner:
        return Response({"error": "You don't have permission to update this purchase"}, 
                        status=status.HTTP_403_FORBIDDEN)
    
    new_status = request.data.get('status')
    if not new_status or new_status not in [s[0] for s in HarvestPurchase.PURCHASE_STATUS]:
        return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Apply status update logic
    purchase.status = new_status
    purchase.save()
    
    # If completed, update listing status
    if new_status == 'completed':
        listing = purchase.listing
        remaining_purchases = HarvestPurchase.objects.filter(
            listing=listing,
            status__in=['pending', 'payment_received']
        ).exists()
        
        if not remaining_purchases:
            listing.status = 'sold'
            listing.save()
    
    serializer = HarvestPurchaseSerializer(purchase)
    return Response(serializer.data)


@api_view(['GET'])
def filter_harvest_listing(request):
    """Filter harvest listings by various parameters"""
    queryset = HarvestListing.objects.filter(status = 'available')
    
    crop_type = request.query_params.get('crop_type')
    if crop_type:
        queryset = queryset.filter(crop_type__name__iexact=crop_type)
    
    location = request.query_params.get('location')
    if location:
        queryset = queryset.filter(location__icontain = location)
    
    min_price = request.query_params.get('min_price')
    if min_price:
        queryset = queryset.filter(price_per_unit__gte=float(min_price))
    
    max_price = request.query_params.get('max_price')
    if max_price:
        queryset = queryset.filter(price_per_unit__lte=float(max_price))
    
    min_quantity = request.query_params.get('min_quantity')
    if min_quantity:
        queryset = queryset.filter(quantity__gte=float(min_quantity))
    
    organic = request.query_params.get('organic')
    if organic and organic.lower() == 'true':
        queryset = queryset.filter(organic_certified=True)
    
    serializer = HarvestListingSerializer(queryset, many=True)
    return Response(serializer.data)


# Equipment Rental Views

@api_view(['GET'])
def all_equipment_rental(request):
    """Get all available equipment rentals"""
    
    today = date.today()
    rental = EquipmentRental.objects.filter(
        status = 'available',
        available_from__lte = today
    ).filter(
        Q(available_until__isnull=True) | Q(available_until__gte=today)
    )
    serializer = EquipmentRentalSerializer(rental, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def my_equipment(request):
    """Get all equipment owned by the current user or add new equipment"""
    
    if request.method=='GET':
        equipment = EquipmentRental.objects.filter(owner = request.user)
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()
        data['owner'] = request.user.id
        serilaizer = EquipmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def equipment_rental(request, equipment_id):
    '''get or create rental listing for specific equipment'''
    try:
        equipment = Equipment.objects.get(pk=equipment_id, owner=request.user)
    except Equipment.DoesNotExist:
        return Response({"error": "Equipment not found or you don't own it"}, 
                        status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        rental = EquipmentRental.objects.filter(equipment=equipment)
        serializer = EquipmentSerializer(rental, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()
        data['equipment'] = equipment.id
        serializer = EquipmentRentalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_equipment(request, rental_id):
    """Book equipment for specific period"""
    try:
        rental = EquipmentRental.objects.get(pk=rental_id, status='available')
    except EquipmentRental.DoesNotExist:
        return Response({"error": "Rental not found or not available"}, 
                        status=status.HTTP_404_NOT_FOUND)  
        
        
    #cannot rent your own equipment
    if rental.equipment.owner == request.user:
        return Response({"error": "You cannot rent your own equipment"}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")
    
    if not start_date or not end_date:
        return Response({"error": "Start date and end date are required"}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
    
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    today = date.today()
    
    if start<today:
        return Response({"error": "Start date cannot be in the past"}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
    if end < start:
        return Response({"error": "End date must be after start date"}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
        
    #calcu the rental duration
    rental_days = (end-start).days+1
    if rental_days < rental.minimum_rental_days:
        return Response({
            "error": f"Minimum rental period is {rental.minimum_rental_days} days"
        }, status=status.HTTP_400_BAD_REQUEST)    
        
    
    conflicting_bookings = RentalBooking.objects.filter(
        rental = rental,
        status__in=['pending', 'active', 'confirm'],
        start_date__lte = end,
        end_date__gte = start
    ).exists()
    
    if conflicting_bookings:
        return Response({"error": "Equipment not available for the selected dates"}, 
                        status=status.HTTP_400_BAD_REQUEST)

    
    #calcu total amt
    
    total_amt = rental.daily_rate * rental_days
    if request.data.get('delivery_loaction') and rental.delivery_available:
        total_amt  += rental.delivery_fee
        
        booking_data = {
        'rental': rental.id,
        'renter': request.user.id,
        'start_date': start_date,
        'end_date': end_date,
        'total_amount': total_amt,
        'delivery_location': request.data.get('delivery_location'),
        'notes': request.data.get('notes', '')
    }
        
    serializer = RentalBookingSerializer(data = booking_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_equipment_bookings(request):
    """get all equipment booking made by current user"""
    booking = RentalBooking.objects.get(rental__equipment__owner=request.user)
    serializer = RentalBookingSerializer(booking, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def received_rental_requests(request):
    """Get all booking requests for the current user's equipment"""
    booking = RentalBooking.objects.filter(rental__equipment__owner=request.user)
    serializer = RentalBookingSerializer(booking, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_booking_status(request, booking_id):
    """update the status of equipment booking"""
    try:
        booking = RentalBooking.object.get(pk=booking_id)
    except RentalBooking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    is_owner = (request.user == booking.rental.equipment.owner)
    is_renter = (request.user == booking.renter)
    
    if not (is_owner or is_renter):
        return Response({"error": "You don't have permission to update this booking"}, 
                        status=status.HTTP_403_FORBIDDEN)
        
    new_status = request.data.get('status')
    if not new_status or new_status not in [s[0] for s in RentalBooking.BOOKING_STATUS]:
        return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
    
    if is_renter or not is_owner and new_status != 'cancelled':
        return Response({"error": "You can only cancel your booking, not change its status"}, 
                        status=status.HTTP_403_FORBIDDEN)
        
    
    booking.status = new_status
    booking.save()
    
    
    if new_status == 'confirmed' or new_status == 'active':
        rental = booking.rental
        rental.status = 'rented'
        rental.save()
        
    elif new_status == 'completed' or new_status == 'cancelled':
        rental = booking.rental
        other_active_bookings = RentalBooking.objects.filter(
            rental=rental, 
            status__in = ['confirmed', 'active']
        ).exclude(pk=booking.id).exists()
        
    if not other_active_bookings:
        rental.status = 'available'
        rental.save()
        
    serializer = RentalBookingSerializer(booking)
    return Response(serializer.data)


@api_view(['GET'])
def filter_equipment_rentals(request):
    """Filter equipment rentals by various parameters"""
    today = date.today()
    queryset = EquipmentRental.objects.filter(
        status='available',
        available_from__lte=today
    ).filter(
        Q(available_until__isnull=True) | Q(available_until__gte=today)
    )
    
    # Apply filters if provided
    category = request.query_params.get('category')
    if category:
        queryset = queryset.filter(equipment__category=category)
    
    location = request.query_params.get('location')
    if location:
        queryset = queryset.filter(location__icontains=location)
    
    min_price = request.query_params.get('min_price')
    if min_price:
        queryset = queryset.filter(daily_rate__gte=float(min_price))
    
    max_price = request.query_params.get('max_price')
    if max_price:
        queryset = queryset.filter(daily_rate__lte=float(max_price))
    
    operator = request.query_params.get('operator_included')
    if operator and operator.lower() == 'true':
        queryset = queryset.filter(operator_included=True)
    
    delivery = request.query_params.get('delivery_available')
    if delivery and delivery.lower() == 'true':
        queryset = queryset.filter(delivery_available=True)
    
    serializer = EquipmentRentalSerializer(queryset, many=True)
    return Response(serializer.data)