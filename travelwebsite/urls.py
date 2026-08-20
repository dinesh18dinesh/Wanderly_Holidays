"""travelwebsite URL Configuration"""
from django.contrib import admin
from .admin_dashboard_views import dashboard
from . import admin_panel_views as ap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Wanderly Travel & Tourism Admin"
admin.site.site_title = "Wanderly Admin"
admin.site.index_title = "Manage Destinations, Packages & Bookings"

urlpatterns = [
    path('admin/', dashboard, name='admin_dashboard'),

    # Users (special-cased: username/password handling)
    path('admin/users/', ap.user_list, name='admin_users_list'),
    path('admin/users/add/', ap.user_add, name='admin_users_add'),
    path('admin/users/<int:pk>/edit/', ap.user_edit, name='admin_users_edit'),
    path('admin/users/<int:pk>/delete/', ap.user_delete, name='admin_users_delete'),

    # Booking travelers (nested under a booking)
    path('admin/bookings/<int:pk>/travelers/', ap.traveler_list, name='admin_travelers_list'),
    path('admin/bookings/<int:pk>/travelers/add/', ap.traveler_add, name='admin_travelers_add'),
    path('admin/bookings/<int:booking_pk>/travelers/<int:pk>/edit/', ap.traveler_edit, name='admin_travelers_edit'),
    path('admin/bookings/<int:booking_pk>/travelers/<int:pk>/delete/', ap.traveler_delete, name='admin_travelers_delete'),

    # Generic section CRUD (bookings, packages, destinations, reviews, enquiries, coupons, newsletter, testimonials, blogposts)
    path('admin/<slug:section>/', ap.section_list, name='admin_section_list'),
    path('admin/<slug:section>/add/', ap.section_add, name='admin_section_add'),
    path('admin/<slug:section>/<int:pk>/edit/', ap.section_edit, name='admin_section_edit'),
    path('admin/<slug:section>/<int:pk>/delete/', ap.section_delete, name='admin_section_delete'),

    path('django-admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
    path('payments/', include('payments.urls')),
    path('', include('destinations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
