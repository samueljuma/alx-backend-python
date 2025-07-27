import django_filters
from chats.models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter messages sent by a specific user
    sender = django_filters.NumberFilter(field_name='sender__id')

    # Filter messages sent after a specific date
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')

    # Filter messages sent before a specific date
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']
