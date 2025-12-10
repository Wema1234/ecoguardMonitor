from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('regular', 'Regular'),
    )
    #table columns
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES) 
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(max_length=500,blank=True, null=True)
    #methods
    def __str__(self):
        return f"{self.username} - {self.email}"
    def is_admin(self):
        return self.user_type == 'admin'
    def is_regular(self):
        return self.user_type == 'regular'