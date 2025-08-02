from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from .models import Message
from django.db.models import Prefetch

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    return HttpResponseForbidden("Invalid request method")


def message_history_view(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    history = message.history.all().order_by('-edited_at')
    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history,
    })


@login_required
def threaded_conversation(request, user_id):
    messages = Message.objects.filter(
        sender=request.user,
        receiver_id=user_id,
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender'))
    )

    return render(request, 'messaging/threaded_conversation.html', {'messages': messages})

@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'messaging/unread_messages.html', {'unread_messages': unread_messages})