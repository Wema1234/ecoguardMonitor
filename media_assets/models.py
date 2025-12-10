from django.db import models
from django.conf import settings
import cloudinary
from cloudinary.models import CloudinaryField

# Create your models here.
class MediaAsset(models.Model):
    # class variable for media assets choices
    CATEGORY_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    )
    # object attributes
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    media_file = CloudinaryField('media',resource_type='auto')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='media_assets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def can_edit(self, user):
        '''check if user can edit the media asset'''
        return user == self.uploaded_by  or user.is_superuser
    def __str__(self):
        return self.title


class EnvironmentalData(models.Model):
    DATA_TYPE_CHOICES = (
        ('air_quality', 'Air Quality'),
        ('waste', 'Waste Management'),
        ('water', 'Water Levels'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='environmental_data')
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Measurement value")
    unit = models.CharField(max_length=50, help_text="Unit of measurement (e.g., ppm, kg, liters)")
    description = models.TextField(blank=True)
    date_recorded = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_recorded']

    def __str__(self):
        return f"{self.data_type} - {self.location} - {self.value} {self.unit}"

    def can_edit(self, user):
        return user == self.user or user.is_superuser or (hasattr(user, 'user_type') and user.user_type == 'admin')
