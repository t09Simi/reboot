from django.contrib import admin
from buddy.models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('role', 'content', 'created_at')
    can_delete = False
    fields = ('role', 'content', 'created_at')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'updated_at', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'role', 'short_content', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('conversation', 'role', 'content', 'tool_calls', 'created_at')

    def short_content(self, obj):
        return obj.content[:80] + ('...' if len(obj.content) > 80 else '')
    short_content.short_description = 'Content'