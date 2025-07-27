# chats/middleware.py
import logging
from datetime import datetime
from datetime import datetime
from django.http import HttpResponseForbidden
import time
from collections import defaultdict
from django.http import JsonResponse

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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_tracker = defaultdict(list)  # {ip: [timestamp1, timestamp2, ...]}

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/messages'):
            ip = self.get_client_ip(request)
            current_time = time.time()

            # Remove timestamps older than 60 seconds
            self.ip_tracker[ip] = [t for t in self.ip_tracker[ip] if current_time - t < 60]

            if len(self.ip_tracker[ip]) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )

            self.ip_tracker[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
