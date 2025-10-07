"""Custom middleware for the API."""

import logging
import traceback
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.response import Response
from api.shared.exceptions.custom_exceptions import CryptoAPIException

logger = logging.getLogger(__name__)


class APIErrorHandlingMiddleware(MiddlewareMixin):
    """Middleware for handling API errors consistently."""
    
    def process_exception(self, request, exception):
        """Handle exceptions in API requests."""
        
        # Log the exception
        logger.exception(f"Unhandled exception in API: {str(exception)}")
        
        # Check if this is an API request
        if request.path.startswith('/api/'):
            if isinstance(exception, CryptoAPIException):
                return JsonResponse({
                    'error': exception.__class__.__name__,
                    'message': str(exception),
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Handle other exceptions
            return JsonResponse({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred',
                'status': 'error',
                'request_id': getattr(request, 'id', None)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Let Django handle non-API requests normally
        return None


class RateLimitMiddleware(MiddlewareMixin):
    """Middleware for rate limiting API requests."""
    
    def process_request(self, request):
        """Check rate limits for API requests."""
        
        if not request.path.startswith('/api/'):
            return None
        
        # Simple rate limiting implementation
        # In production, this would use Redis or similar
        client_ip = self.get_client_ip(request)
        
        # Check rate limit (placeholder implementation)
        if self.is_rate_limited(client_ip):
            return JsonResponse({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests from this IP',
                'status': 'error'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        return None
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_rate_limited(self, client_ip):
        """Check if client is rate limited."""
        # Placeholder implementation
        # In production, this would check against Redis
        return False


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware for logging API requests."""
    
    def process_request(self, request):
        """Log incoming API requests."""
        if request.path.startswith('/api/'):
            logger.info(f"API Request: {request.method} {request.path} from {self.get_client_ip(request)}")
    
    def process_response(self, request, response):
        """Log API responses."""
        if request.path.startswith('/api/'):
            logger.info(f"API Response: {response.status_code} for {request.method} {request.path}")
        return response
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
