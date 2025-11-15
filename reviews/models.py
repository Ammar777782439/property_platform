from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Property


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='property_reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['property', 'user'], name='unique_review_per_user_property')
        ]

    def __str__(self):
        return f"Review {self.rating}★ by {self.user} on {self.property}"
