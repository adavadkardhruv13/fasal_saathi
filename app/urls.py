from django.urls import path
from .views import storage, crop 

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
]