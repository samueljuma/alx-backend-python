# chats/middleware.py
import logging
from datetime import datetime
from datetime import datetime
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log') 
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current hour (24-hour format)
        current_hour = datetime.now().hour

        # Deny access outside 6PM–9PM (18–21)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Chat access is only allowed between 6PM and 9PM.")

        return self.get_response(request)
