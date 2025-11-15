from django.contrib import admin
from .models import User, PropertyOwner, Notification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_role', 'status', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('user_role', 'status', 'is_active')


@admin.register(PropertyOwner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'license_status', 'registration_status')
    search_fields = ('user__username', 'license_number')
    list_filter = ('license_status', 'registration_status')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'user', 'is_read', 'created_at')
    search_fields = ('type_name', 'message', 'user__username')
