from django.contrib import admin
from .models import PropertyType, Amenity, Property, PropertyImage, PropertyAmenity


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'created_at')


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('amenity_name', 'created_at')


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'default_daily_price', 'status', 'owner')
    list_filter = ('city', 'status')
    search_fields = ('name', 'city', 'address')
    inlines = [PropertyImageInline]


@admin.register(PropertyAmenity)
class PropertyAmenityAdmin(admin.ModelAdmin):
    list_display = ('property', 'amenity', 'is_included_in_price', 'extra_cost')
