from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('additional info', {'fields': ('user_type', 'profile_picture', 'bio')}),
        
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('additional info', {'fields': ('user_type')}),
    )
