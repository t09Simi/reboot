from django.contrib import admin
from .models import MentorshipRequest

# Register your models here.
@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'message', 'created_at']