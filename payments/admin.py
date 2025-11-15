from django.contrib import admin
from .models import PaymentMethod, Payment


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('method_name', 'owner', 'property', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('method_name', 'owner__user__username')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'booking', 'amount', 'status', 'payment_date')
    list_filter = ('status',)
    search_fields = ('booking__user__username', 'transaction_id')
