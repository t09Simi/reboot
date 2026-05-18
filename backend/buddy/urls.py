from django.urls import path

from buddy.views import (
    SendMessageView,
    ListConversationsView,
    ConversationDetailView,
)


app_name = 'buddy'

urlpatterns = [
    path('conversations/', ListConversationsView.as_view(), name='list-conversations'),
    path('conversations/<str:conversation_id>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/<str:conversation_id>/messages/', SendMessageView.as_view(), name='send-message'),
]