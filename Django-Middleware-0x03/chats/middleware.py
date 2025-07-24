import logging
from django.http import HttpResponseForbidden, JsonResponse
from django.core.cache import cache
from datetime import datetime, time, timedelta
from django.conf import settings

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
        # Get configuration from settings or use defaults
        self.restricted_start = getattr(settings, 'RESTRICTED_START', time(21, 0))  # 9 PM default
        self.restricted_end = getattr(settings, 'RESTRICTED_END', time(6, 0))       # 6 AM default
        self.restricted_paths = getattr(settings, 'RESTRICTED_PATHS', ['/chat/', '/messages/', '/api/chat/'])

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
        
        if is_restricted and is_chat_url and not (hasattr(request.user, 'is_staff') and request.user.is_staff):
            return JsonResponse(
                {
                    "error": "Chat access is restricted between 9 PM and 6 AM. "
                            "Please try again during allowed hours.",
                    "status": 403
                },
                status=403
            )
        
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('offensive_language')
        # Get configuration from settings or use defaults
        self.RATE_LIMIT = getattr(settings, 'RATE_LIMIT', 5)  # 5 messages default
        self.TIME_WINDOW = getattr(settings, 'TIME_WINDOW', 60)  # 60 seconds default
        self.MESSAGE_PATHS = getattr(settings, 'MESSAGE_PATHS', ['/api/messages/', '/chat/send/'])

    def __call__(self, request):
        # Only process POST requests to message endpoints
        if request.method == 'POST' and any(
            request.path.startswith(path) for path in self.MESSAGE_PATHS
        ):
            ip_address = self._get_client_ip(request)
            cache_key = f"rate_limit_{ip_address}"

            # Get current count or initialize
            request_count = cache.get(cache_key, 0)
            
            if request_count >= self.RATE_LIMIT:
                self.logger.warning(
                    f"Rate limit exceeded for IP: {ip_address} - "
                    f"{request_count} requests in last {self.TIME_WINDOW} seconds"
                )
                return JsonResponse(
                    {
                        "error": "Rate limit exceeded. "
                                "Please wait before sending more messages.",
                        "status": 429
                    },
                    status=429
                )

            # Increment count and set/update cache
            cache.set(
                key=cache_key,
                value=request_count + 1,
                timeout=self.TIME_WINDOW
            )

        return self.get_response(request)

    def _get_client_ip(self, request):
        """Extract client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')