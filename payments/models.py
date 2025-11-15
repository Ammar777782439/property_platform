from django.db import models
import uuid


class PaymentMethod(models.Model):
    method_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('accounts.PropertyOwner', on_delete=models.CASCADE, related_name='payment_methods', verbose_name='المالك')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='payment_methods', null=True, blank=True, verbose_name='العقار (اختياري)')
    method_name = models.CharField(max_length=100, verbose_name='اسم الطريقة')
    account_details = models.TextField(verbose_name='تفاصيل الحساب')
    instructions = models.TextField(blank=True, null=True, verbose_name='تعليمات الدفع')
    is_active = models.BooleanField(default=True, verbose_name='نشطة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    def __str__(self):
        return f"{self.method_name}"

    class Meta:
        db_table = 'payment_method'
        verbose_name = 'طريقة دفع'
        verbose_name_plural = 'طرق الدفع'


class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='payments', verbose_name='الحجز')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, verbose_name='طريقة الدفع')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المبلغ')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الدفع')
    transaction_id = models.CharField(max_length=100, unique=True, verbose_name='معرف المعاملة')
    status = models.CharField(max_length=20, choices=[('completed','مكتمل'),('failed','فشل'),('pending','معلق')], default='pending', verbose_name='حالة الدفع')
    notes = models.TextField(null=True, blank=True, verbose_name='ملاحظات')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    def __str__(self):
        return f"دفعة {self.amount} - {self.booking}"

    class Meta:
        db_table = 'payment'
        verbose_name = 'دفعة'
        verbose_name_plural = 'الدفعات'
