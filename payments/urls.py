from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.initiate_payment, name='initiate_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('verify/', views.verify_payment, name='verify_payment'),
    path('failed/', views.payment_failed, name='payment_failed'),
]
