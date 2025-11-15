from django.contrib import admin
from .models import Offers, Availability, Booking, BookingDay


@admin.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active', 'start_date', 'end_date')
    search_fields = ('code', 'description')
    list_filter = ('is_active',)


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('property', 'date', 'is_available', 'blocked_by_owner')
    list_filter = ('is_available', 'blocked_by_owner')
    search_fields = ('property__name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'property', 'start_date', 'end_date', 'status', 'payment_status', 'total_price')
    list_filter = ('status', 'payment_status')
    search_fields = ('user__username', 'property__name')


@admin.register(BookingDay)
class BookingDayAdmin(admin.ModelAdmin):
    list_display = ('booking', 'date', 'property')
