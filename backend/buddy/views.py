"""
API endpoints for the AI Career Buddy.
"""

import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from buddy.models import Conversation, Message
from buddy.services import _generate_reply


logger = logging.getLogger(__name__)

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, conversation_id):
        user_message = request.data.get('message','').strip()
        if not user_message:
            return Response(
                {"error": "Message cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if conversation_id == 'new':
            conversation = Conversation.objects.create(
                user=request.user,
                title=user_message[:80],   # auto-title from first message
            )
        else:
            try:
                conversation = Conversation.objects.get(
                    pk = conversation_id,
                    user = request.user
                )
            except Conversation.DoesNotExist:
                return Response(
                    {"error": "Conversation not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            
        try:
            reply = _generate_reply(conversation, user_message)
        except Exception as e:
            logger.exception("Buddy reply generation failed")
            return Response(
                {"error": "The AI buddy is temporarily unavailable. Please try again."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        
        return Response({
            "conversation_id": conversation.pk,
            "title": conversation.title,
            "reply": reply,
        }, status=status.HTTP_200_OK)
    
class ListConversationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversations = Conversation.objects.filter(user=request.user)
        data = [
            {
                "id": c.pk,
                "title": c.title,
                "updated_at": c.updated_at,
                "message_count": c.messages.count(),
            }
            for c in conversations
        ]
        return Response(data)
    
class ConversationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(
                pk=conversation_id,
                user=request.user,
            )
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        messages = [
            {
                "id": m.pk,
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at,
            }
            for m in conversation.messages.all()
        ]

        return Response({
            "id": conversation.pk,
            "title": conversation.title,
            "messages": messages,
        })
