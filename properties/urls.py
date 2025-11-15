from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='home'),
    path('property/<uuid:property_id>/', views.property_detail, name='property_detail'),
]
