from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to access or modify messages in that conversation.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users to access the API at all
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed only to participants of the conversation
        # Assuming obj is a Message or Conversation instance with participants attribute

        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            return request.user in obj.participants.all()

        # For write permissions (POST, PUT, DELETE), also check user is participant
        return request.user in obj.participants.all()
