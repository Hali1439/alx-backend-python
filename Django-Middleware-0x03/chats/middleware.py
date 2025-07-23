import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logging
        self.logger = logging.getLogger('request_logger')
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        handler = logging.FileHandler('requests.log')
        handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(handler)

    def __call__(self, request):
        # Get the user (or 'Anonymous' if not authenticated)
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        
        # Log the request
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        
        # Process the request
        response = self.get_response(request)
        
        return response
