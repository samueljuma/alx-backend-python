from django.db import models

from django.db import models
from django.conf import settings

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )
    read = models.BooleanField(default=False)

    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

    def is_reply(self):
        return self.parent_message is not None



class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} on message {self.message.id}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='edited_messages')
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit history of message {self.message.id} at {self.edited_at}"
