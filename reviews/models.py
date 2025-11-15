from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    message = models.TextField(verbose_name='رسالة المراجعة')
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, verbose_name='الحجز')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='reviews', verbose_name='العقار')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reviews', verbose_name='المستخدم')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='التقييم')
    comment = models.CharField(max_length=500, verbose_name='التعليق')

    def __str__(self):
        return f"مراجعة {self.user} - {self.property}"

    class Meta:
        db_table = 'review'
        verbose_name = 'مراجعة'
        verbose_name_plural = 'المراجعات'
        unique_together = ('user', 'booking', 'property')
