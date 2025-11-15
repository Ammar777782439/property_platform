from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta
import uuid
import builtins


class Offers(models.Model):
    offers_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, null=True, blank=True, verbose_name='العقار (اختياري)')
    code = models.CharField(max_length=50, unique=True, verbose_name='رمز العرض')
    description = models.TextField(verbose_name='وصف العرض')
    discount_type = models.CharField(max_length=20, choices=[('percentage','نسبة مئوية'), ('fixed_amount','مبلغ ثابت')], verbose_name='نوع الخصم')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='قيمة الخصم')
    start_date = models.DateField(verbose_name='تاريخ البداية')
    end_date = models.DateField(verbose_name='تاريخ النهاية')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    usage_limit = models.PositiveIntegerField(null=True, blank=True, verbose_name='حد الاستخدام')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        db_table = 'offers'
        verbose_name = 'عرض'
        verbose_name_plural = 'العروض'

    def __str__(self):
        return f"عرض: {self.code}"

    @builtins.property
    def is_valid(self):
        today = date.today()
        return self.is_active and self.start_date <= today <= self.end_date

    def calculate_discount(self, original_price):
        if self.discount_type == 'percentage':
            return (original_price * self.discount_value) / 100
        return self.discount_value


class Availability(models.Model):
    availability_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='availability', verbose_name='العقار')
    date = models.DateField(verbose_name='التاريخ')
    is_available = models.BooleanField(default=True, verbose_name='متاح')
    blocked_by_booking = models.ForeignKey('Booking', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='محجوز بواسطة')
    blocked_by_owner = models.BooleanField(default=False, verbose_name='محجوز بواسطة المالك')
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='سعر خاص')
    is_tentative = models.BooleanField(default=False, verbose_name='حجز مؤقت')
    hold_expiry = models.DateTimeField(null=True, blank=True, verbose_name='انتهاء الحجز المؤقت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        db_table = 'availability'
        verbose_name = 'توفر'
        verbose_name_plural = 'التوفر'
        unique_together = ('property', 'date')

    def __str__(self):
        return f"{self.property} - {self.date}"


class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('pending_owner_approval', 'في انتظار موافقة المالك'),
        ('confirmed', 'مؤكد'),
        ('rejected_by_owner', 'مرفوض من المالك'),
        ('cancelled_by_user', 'ملغي من المستخدم'),
        ('cancelled_by_owner', 'ملغي من المالك'),
        ('completed', 'مكتمل'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'معلق'),
        ('paid', 'مدفوع'),
        ('partially_paid', 'مدفوع جزئياً'),
        ('refunded', 'مسترد'),
        ('failed', 'فشل'),
    ]

    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='bookings', verbose_name='المستخدم')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='bookings', verbose_name='العقار')
    offers = models.ForeignKey(Offers, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='العرض المطبق')
    start_date = models.DateField(verbose_name='تاريخ البداية')
    end_date = models.DateField(verbose_name='تاريخ النهاية')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر الأصلي')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='مبلغ الخصم')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر الإجمالي')
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الحجز')
    status = models.CharField(max_length=30, choices=BOOKING_STATUS_CHOICES, default='pending_owner_approval', verbose_name='حالة الحجز')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name='حالة الدفع')
    owner_response = models.DateTimeField(null=True, blank=True, verbose_name='استجابة المالك')
    rejection_reason = models.TextField(null=True, blank=True, verbose_name='سبب الرفض')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        db_table = 'booking'
        verbose_name = 'حجز'
        verbose_name_plural = 'الحجوزات'
        ordering = ['-created_at']

    def __str__(self):
        return f"حجز {self.user} - {self.property}"

    @builtins.property
    def duration_days(self):
        return (self.end_date - self.start_date).days

    @builtins.property
    def can_be_cancelled(self):
        cancel_deadline = self.start_date - timedelta(days=1)
        return date.today() <= cancel_deadline and self.status in ['confirmed', 'pending_owner_approval']

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('Invalid date range')
        qs = Booking.objects.filter(property=self.property, status__in=['pending_owner_approval', 'confirmed']).exclude(pk=self.pk)
        overlap = qs.filter(start_date__lt=self.end_date, end_date__gt=self.start_date).exists()
        if overlap:
            raise ValidationError('Selected dates are not available')


class BookingDay(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name='الحجز')
    date = models.DateField(verbose_name='التاريخ')
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, verbose_name='التوفر')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, verbose_name='العقار')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        db_table = 'booking_day'
        verbose_name = 'يوم حجز'
        verbose_name_plural = 'أيام الحجوزات'
        unique_together = ('booking', 'date')

    def __str__(self):
        return f"{self.booking} - {self.date}"
