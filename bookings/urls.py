from django.urls import path
from . import views
urlpatterns=[
 path('book/<slug:slug>/',views.book_package,name='book_package'),
 path('my-bookings/',views.my_bookings,name='my_bookings'),
 path('edit/<str:booking_id>/',views.edit_booking,name='edit_booking'),
 path('travellers/',views.saved_travelers,name='saved_travelers'),
 path('travellers/save/',views.save_traveler,name='save_traveler'),
 path('travellers/<int:traveler_id>/json/',views.traveler_data_api,name='traveler_data_api'),
 path('cancel/<str:booking_id>/',views.cancel_booking,name='cancel_booking'),
 path('invoice/<str:booking_id>/',views.download_invoice,name='download_invoice'),
]
