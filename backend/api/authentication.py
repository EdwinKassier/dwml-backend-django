"""Custom authentication classes for the API."""

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
import jwt
from datetime import datetime


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication for API endpoints.
    """
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            if not user_id:
                raise AuthenticationFailed('Invalid token')
            
            # In a real implementation, you would fetch the user from the database
            # For now, we'll create a simple user object
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found')
            
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')


class APIKeyAuthentication(BaseAuthentication):
    """
    Simple API key authentication for service-to-service communication.
    """
    
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        
        if not api_key:
            return None
        
        # In a real implementation, you would validate against a database
        # For now, we'll use a simple check against settings
        if api_key == getattr(settings, 'API_KEY', 'default-api-key'):
            return (AnonymousUser(), api_key)
        
        return None
