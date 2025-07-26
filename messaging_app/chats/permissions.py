# messaging_app/chats/permissions.py
from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated 

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if hasattr(obj, 'conversation'):
            is_participant = request.user in obj.conversation.participants.all()
        elif isinstance(obj, Conversation):
            is_participant = request.user in obj.participants.all()
        else:
            return False

        # Allow only participants to perform unsafe methods
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return is_participant

        # Safe methods are GET, HEAD, OPTIONS
        return True
