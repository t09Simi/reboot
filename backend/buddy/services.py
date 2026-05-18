"""
Claude API service for the AI Career Buddy.

Wraps the Anthropic client and handles converting Reboot's Message model
into the format Claude's API expects.
"""

import logging

from anthropic import Anthropic, APIError
from django.conf import settings

from buddy.models import Message


logger = logging.getLogger(__name__)


# Model choice — Haiku 4.5 is fast and cheap. Upgrade to Sonnet if quality matters more.
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# Cap how much history we send. 20 messages = ~10 exchanges, plenty for context
# without bloating every API call.
MAX_HISTORY_MESSAGES = 20

# Cap response length. Prevents runaway costs and keeps responses concise.
MAX_OUTPUT_TOKENS = 1024


SYSTEM_PROMPT = """You are the AI Career Buddy for Reboot — a platform helping career gapers and self-taught beginners break into tech.

Your role:
- Provide warm, practical, judgment-free career advice
- Help users identify skills to learn, roles to target, and how to position their experience
- Be specific and actionable; avoid generic motivation
- If asked something you don't know about the user specifically, ask them rather than assume

Tone: encouraging but honest. Like a senior engineer who genuinely wants to help, not a corporate coach.

Keep responses focused. If someone asks a broad question, suggest narrowing it down.
"""
def _get_client()-> Anthropic:
    """Returns a configured Anthropic client. Raises if API key is missing."""
    api_key = settings.ANTHROPIC_API_KEY
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not configured")
    return Anthropic(api_key=api_key)

def _build_messages_payload(conversation) -> list[dict]:
    """
    Convert a Conversation's stored Messages into Claude's API format.
    
    Claude expects messages alternating user/assistant. We send up to
    MAX_HISTORY_MESSAGES of the most recent messages.
    """
    recent_messages = (
        conversation.messages
        .filter(role__in=[Message.Role.USER, Message.Role.ASSISTANT])
        .order_by('-created_at')[:MAX_HISTORY_MESSAGES]
    )

    recent_messages = list(reversed(list(recent_messages)))

    return[
        {"role":msg.role, "content": msg.content}
        for msg in recent_messages
    ]

def _generate_reply(conversation, user_message_text:str) -> str:
    """
    Save the user's message, call Claude, save and return the assistant reply.
    
    Returns the assistant's reply text. Raises on API failure.
    """
    Message.objects.create(
        conversation=conversation,
        role= Message.Role.USER,
        content=user_message_text
    )

    messages_payload = _build_messages_payload(conversation)

    client = _get_client()
    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_OUTPUT_TOKENS,
            system=SYSTEM_PROMPT,
            messages=messages_payload,
        )
    except APIError as e:
        logger.exception("Claude API call failed for conversation %s", conversation.pk)
        raise

    reply_text = "".join(
        block.text for block in response.content if block.type == "text"
    )

    Message.objects.create(
        conversation=conversation,
        role=Message.Role.ASSISTANT,
        content=reply_text,
    )

    conversation.save()

    return reply_text