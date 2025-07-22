from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(ModelViewSet):
    """
    ViewSet for listing and creating conversations
    """
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Limit conversations to those where the requesting user is a participant
        """
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with given participant user IDs
        """
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response({"error": "Participants required"}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        users = User.objects.filter(user_id__in=participant_ids)  # Assuming custom user_id field
        conversation.participants.set(users)
        conversation.participants.add(request.user)  # Optionally ensure the creator is included
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(ModelViewSet):
    """
    ViewSet for listing, creating, and managing messages
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    def get_queryset(self):
        """
        Only return messages from conversations the user is a participant of
        """
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new message in a conversation
        """
        conversation_id = request.data.get("conversation")
        sender_id = request.data.get("sender")
        message_body = request.data.get("message_body")

        if not all([conversation_id, sender_id, message_body]):
            return Response(
                {"error": "conversation, sender, and message_body fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            sender = User.objects.get(user_id=sender_id)  # Assuming custom user_id field
        except (Conversation.DoesNotExist, User.DoesNotExist):
            return Response({"error": "Invalid conversation or sender ID"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user != sender:
            return Response({"error": "Authenticated user must be the sender"}, status=status.HTTP_403_FORBIDDEN)

        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant of this conversation"}, status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
