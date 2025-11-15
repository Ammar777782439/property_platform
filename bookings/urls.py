from django.urls import path
from . import views

urlpatterns = [
    path('create/<uuid:property_id>/', views.create_booking, name='create_booking'),
    path('confirm/<uuid:booking_id>/', views.booking_confirm, name='booking_confirm'),
]
