from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from rest_framework import filters

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants')

        if not participant_ids or len(participant_ids) < 2:
            return Response(
                {"error": "At least two participants are required to start a conversation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']


    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk') 

        qs = Message.objects.all().select_related('sender', 'conversation')

        if conversation_id:
            qs = qs.filter(conversation__conversation_id=conversation_id)

        return qs.order_by('sent_at')


    def create(self, request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_pk')
        sender_id = request.data.get('sender')

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        message = Message.objects.create(
            conversation=conversation,
            sender_id=sender_id,
            message_body=request.data.get('message_body')
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

