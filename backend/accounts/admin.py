from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,CareerGapProfile, MentorProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Reboot Info', {'fields': ('name', 'role', 'phone')}),
    )

@admin.register(CareerGapProfile)
class CareerGaperProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employment_status', 'gap_duration')

@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display =('user', 'company', 'years_of_experience', 'availability')

