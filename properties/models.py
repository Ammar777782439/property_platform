from django.db import models
import uuid


class PropertyType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100, unique=True, verbose_name='اسم النوع')
    description = models.TextField(blank=True, null=True, verbose_name='الوصف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    def __str__(self):
        return self.type_name

    class Meta:
        db_table = 'property_type'
        verbose_name = 'نوع عقار'
        verbose_name_plural = 'أنواع العقارات'


class Amenity(models.Model):
    amenity_id = models.AutoField(primary_key=True)
    amenity_name = models.CharField(max_length=100, unique=True, verbose_name='اسم المرفق')
    description = models.TextField(blank=True, null=True, verbose_name='الوصف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    def __str__(self):
        return self.amenity_name

    class Meta:
        db_table = 'amenity'
        verbose_name = 'مرفق'
        verbose_name_plural = 'المرافق'


class Property(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('accounts.PropertyOwner', on_delete=models.CASCADE, related_name='properties', verbose_name='المالك')
    type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, related_name='properties', verbose_name='نوع العقار')
    name = models.CharField(max_length=200, verbose_name='اسم العقار')
    description = models.TextField(verbose_name='الوصف')
    address = models.CharField(max_length=300, verbose_name='العنوان')
    city = models.CharField(max_length=100, verbose_name='المدينة')
    country = models.CharField(max_length=100, default='السعودية', verbose_name='البلد')
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True, verbose_name='خط العرض')
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True, verbose_name='خط الطول')
    status = models.CharField(max_length=20, choices=[('active','نشط'),('inactive','غير نشط'),('under_maintenance','تحت الصيانة')], default='active', verbose_name='حالة العقار')
    max_capacity = models.PositiveIntegerField(verbose_name='الحد الأقصى للإقامة')
    default_daily_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر اليومي الافتراضي')
    check_in_time = models.TimeField(default='15:00:00', verbose_name='وقت تسجيل الدخول')
    check_out_time = models.TimeField(default='11:00:00', verbose_name='وقت تسجيل الخروج')
    is_child_friendly = models.BooleanField(default=False, verbose_name='مناسب للأطفال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    def __str__(self):
        return f"{self.name} - {self.city}"

    class Meta:
        db_table = 'property'
        verbose_name = 'عقار'
        verbose_name_plural = 'العقارات'

    @property
    def main_image(self):
        return self.images.filter(is_main_image=True).first()


class PropertyImage(models.Model):
    image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images', verbose_name='العقار')
    image_url = models.URLField(verbose_name='رابط الصورة')
    description = models.TextField(blank=True, null=True, verbose_name='الوصف')
    is_main_image = models.BooleanField(default=False, verbose_name='صورة رئيسية')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الرفع')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    def __str__(self):
        return f"صورة للعقار: {self.property.name}"

    class Meta:
        db_table = 'property_image'
        verbose_name = 'صورة عقار'
        verbose_name_plural = 'صور العقارات'

    def save(self, *args, **kwargs):
        if self.is_main_image:
            PropertyImage.objects.filter(property=self.property, is_main_image=True).exclude(pk=self.pk).update(is_main_image=False)
        super().save(*args, **kwargs)


class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name='العقار')
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE, verbose_name='المرفق')
    is_included_in_price = models.BooleanField(default=True, verbose_name='مشمول في السعر')
    extra_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='تكلفة إضافية')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    def __str__(self):
        return f"{self.property.name} - {self.amenity.amenity_name}"

    class Meta:
        db_table = 'property_amenity'
        verbose_name = 'مرفق عقار'
        verbose_name_plural = 'مرافق العقارات'
        unique_together = ('property', 'amenity')
