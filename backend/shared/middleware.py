"""Global error handling middleware."""

import logging

from django.http import JsonResponse
from rest_framework import status

from .exceptions.custom_exceptions import (
    DomainException,
    ExternalServiceError,
    NotFoundError,
    ValidationError,
)

logger = logging.getLogger(__name__)


class DomainExceptionMiddleware:
    """
    Middleware to catch domain exceptions and return appropriate HTTP responses.

    This keeps views clean - they don't need try-except blocks.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """Handle domain exceptions."""

        # ValidationError -> 400 Bad Request
        if isinstance(exception, ValidationError):
            return JsonResponse(
                {"error": exception.message, "code": exception.code},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # NotFoundError -> 404 Not Found
        if isinstance(exception, NotFoundError):
            return JsonResponse(
                {"error": exception.message, "code": exception.code},
                status=status.HTTP_404_NOT_FOUND,
            )

        # ExternalServiceError -> 503 Service Unavailable
        if isinstance(exception, ExternalServiceError):
            logger.error(f"External service error: {exception.message}")
            return JsonResponse(
                {"error": "Service temporarily unavailable", "code": exception.code},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # Other DomainExceptions -> 500 Internal Server Error
        if isinstance(exception, DomainException):
            logger.error(f"Domain exception: {exception.message}")
            return JsonResponse(
                {"error": "Internal error", "code": exception.code},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Let Django handle other exceptions
        return None
