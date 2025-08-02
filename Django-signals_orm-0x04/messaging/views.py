from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    return HttpResponseForbidden("Invalid request method")
