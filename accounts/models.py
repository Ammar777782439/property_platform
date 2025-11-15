from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


USER_ROLE_CHOICES = [
    ('admin', 'مدير النظام'),
    ('owner', 'مالك عقار'),
    ('customer', 'عميل'),
]

USER_STATUS_CHOICES = [
    ('active', 'نشط'),
    ('inactive', 'غير نشط'),
    ('blocked', 'محظور'),
    ('pending_approval', 'في انتظار الموافقة'),
]

LICENSE_STATUS_CHOICES = [
    ('licensed', 'مرخص'),
    ('unlicensed', 'غير مرخص'),
    ('pending_review', 'قيد المراجعة'),
]

REGISTRATION_STATUS_CHOICES = [
    ('pending_approval', 'في انتظار الموافقة'),
    ('approved', 'موافق عليه'),
    ('rejected', 'مرفوض'),
]


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, verbose_name='الاسم الأول')
    last_name = models.CharField(max_length=100, verbose_name='الاسم الأخير')
    email = models.EmailField(unique=True, verbose_name='البريد الإلكتروني')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='رقم الهاتف')
    user_role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='customer', verbose_name='دور المستخدم')
    status = models.CharField(max_length=20, choices=USER_STATUS_CHOICES, default='active', verbose_name='حالة الحساب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    def get_full_name_ar(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self):
        return self.user_role == 'admin'

    @property
    def is_owner(self):
        return self.user_role == 'owner'

    @property
    def is_customer(self):
        return self.user_role == 'customer'

    class Meta:
        db_table = 'user'
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمين'


class PropertyOwner(models.Model):
    owner_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='property_owner_profile', verbose_name='المستخدم')
    license_number = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name='رقم الترخيص')
    organization_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='اسم المنظمة')
    license_status = models.CharField(max_length=20, choices=LICENSE_STATUS_CHOICES, default='unlicensed', verbose_name='حالة الترخيص')
    registration_status = models.CharField(max_length=20, choices=REGISTRATION_STATUS_CHOICES, default='pending_approval', verbose_name='حالة التسجيل')
    approved_by_user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_owners', verbose_name='تم الموافقة بواسطة')
    approval_date = models.DateTimeField(null=True, blank=True, verbose_name='تاريخ الموافقة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    def __str__(self):
        return f"مالك: {self.user.get_full_name_ar()} - الترخيص: {self.license_number or 'غير محدد'}"

    @property
    def is_approved(self):
        return self.registration_status == 'approved'

    class Meta:
        db_table = 'property_owner'
        verbose_name = 'مالك عقار'
        verbose_name_plural = 'مالكو العقارات'


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100, unique=True, verbose_name='نوع الإشعار')
    message = models.TextField(verbose_name='رسالة الإشعار')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications', verbose_name='المستخدم')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    is_read = models.BooleanField(default=False, verbose_name='مقروء')

    def __str__(self):
        return f"إشعار {self.type_name} - {self.user.get_full_name_ar()}"

    class Meta:
        db_table = 'notification'
        verbose_name = 'إشعار'
        verbose_name_plural = 'الإشعارات'
