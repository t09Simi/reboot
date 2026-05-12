from django.contrib import admin
from .models import MentorshipRequest, Session

# Register your models here.
@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'message', 'created_at']

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'career_gaper', 'request', 'scheduled_at', 'duration', 'meeting_link', 'status', 'created_at']