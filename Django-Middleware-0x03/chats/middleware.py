import logging
from django.http import HttpResponseForbidden, JsonResponse
from datetime import datetime, time  # Added time import here

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = self._configure_logger()

    def _configure_logger(self):
        """Helper method to configure the logger"""
        logger = logging.getLogger('request_logger')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler('requests.log')
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter('%(message)s'))
        
        logger.addHandler(handler)
        return logger

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path} - Method: {request.method}"
        self.logger.info(log_message)
        
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.restricted_start = time(21, 0)  # 9 PM
        self.restricted_end = time(6, 0)    # 6 AM
        self.restricted_paths = ['/chat/', '/messages/', '/api/chat/']

    def __call__(self, request):
        current_time = datetime.now().time()
        
        is_restricted = (
            (current_time >= self.restricted_start) or
            (current_time <= self.restricted_end)
        )
        
        is_chat_url = any(
            request.path.startswith(path)
            for path in self.restricted_paths
        )
        
        if is_restricted and is_chat_url:
            return HttpResponseForbidden(
                "Chat access is restricted between 9 PM and 6 AM. "
                "Please try again during allowed hours."
            )
        
        return self.get_response(request)