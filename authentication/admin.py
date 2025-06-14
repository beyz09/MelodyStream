from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'premium_status', 'birth_date', 'gender')
    fieldsets = UserAdmin.fieldsets + (('Ek Bilgiler', {'fields': ('birth_date', 'gender', 'premium_status', 'profile_image')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Ek Bilgiler', {'fields': ('birth_date', 'gender', 'premium_status', 'profile_image')}),) 