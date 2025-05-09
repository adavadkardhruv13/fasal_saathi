from django.urls import path
from .views import storage, crop, marketplace


urlpatterns = [
    path('api/storage/', storage.view_all_storages, name='view_all_storages'),
    path('api/storage/add', storage.add_storage, name='add_storage'),
    #path('api/storage/<int:pk>/active_booking/', storage.view_storgae_with_active_booking, name='view_storgae_with_active_booking'),
    path('api/storage/<int:pk>', storage.perticular_storage_details, name='perticular_storage_details'),
    path('api/crops/<str:crop_name>/', crop.cropInfo, name='cropInfo'),
    path('api/crops/', crop.allcrop, name='cropInfo'),
    path('api/storage/filter/availability/', storage.storage_space_availability_filter, name='storage-availability-filter'),
    path('api/storage/filter/type/', storage.storage_space_type_filter, name='storage-type-filter'),
    path('api/storage/filter/capacity/', storage.storage_space_capacity_filter, name='storage-capacity-filter'),
    path('api/storage/book/<int:id>/', storage.book_storage, name='book_storage_space'),
    path('api/storage/search/', storage.search_storage, name='search_storage'),
    
    path('api/marketplace/harvests/', marketplace.all_harvest_listings, name='all-harvest-listings'),
    path('api/marketplace/harvests/filter/', marketplace.filter_harvest_listings, name='filter-harvest-listings'),
    path('api/marketplace/my-harvests/', marketplace.farmer_harvest_listings, name='my-harvest-listings'),
    path('api/marketplace/harvests/<int:pk>/', marketplace.harvest_listing_detail, name='harvest-detail'),
    path('api/marketplace/harvests/<int:listing_id>/purchase/', marketplace.purchase_harvest, name='purchase-harvest'),
    path('api/marketplace/my-purchases/', marketplace.my_harvest_purchases, name='my-purchases'),
    path('api/marketplace/my-sales/', marketplace.my_harvest_sales, name='my-sales'),
    path('api/marketplace/purchases/<int:purchase_id>/status/', marketplace.update_purchase_status, name='update-purchase-status'),
    
    # Equipment Rental URLs
    path('api/marketplace/equipment-rentals/', marketplace.all_equipment_rentals, name='all-equipment-rentals'),
    path('api/marketplace/equipment-rentals/filter/', marketplace.filter_equipment_rentals, name='filter-equipment-rentals'),
    path('api/marketplace/my-equipment/', marketplace.my_equipment, name='my-equipment'),
    path('api/marketplace/my-equipment/<int:equipment_id>/rentals/', marketplace.equipment_rentals, name='equipment-rentals'),
    path('api/marketplace/equipment-rentals/<int:rental_id>/book/', marketplace.book_equipment, name='book-equipment'),
    path('api/marketplace/my-bookings/', marketplace.my_equipment_bookings, name='my-bookings'),
]