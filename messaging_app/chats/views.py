from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations
    """
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

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
        if not isinstance(participant_ids, list):
            return Response(
                {"error": "Participants should be a list of user IDs"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure creator is always included
        if request.user.id not in participant_ids:
            participant_ids.append(request.user.id)

        try:
            users = User.objects.filter(id__in=participant_ids)
            if users.count() != len(participant_ids):
                raise User.DoesNotExist
        except User.DoesNotExist:
            return Response(
                {"error": "One or more participant IDs are invalid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and managing messages
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conversation_id']  # Added conversation_id filter
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    def get_queryset(self):
        """
        Only return messages from conversations the user is a participant of
        """
        queryset = Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation')
        
        # Filter by conversation_id if provided in query params
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
            
        return queryset

    def perform_create(self, serializer):
        """
        Automatically set the sender to the current user
        and verify conversation participation
        """
        conversation_id = serializer.validated_data.get('conversation_id')
        if not conversation_id:
            raise serializers.ValidationError({"conversation_id": "This field is required"})
            
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation does not exist")

        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You are not a participant of this conversation")
            
        serializer.save(sender=self.request.user, conversation=conversation)

    def create(self, request, *args, **kwargs):
        """
        Custom create method with validation
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except (PermissionDenied, serializers.ValidationError) as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN if isinstance(e, PermissionDenied) 
                else status.HTTP_400_BAD_REQUEST
            )
