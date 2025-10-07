"""Backwards compatibility views for legacy endpoints."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .portfolio import process_request as new_process_request
from .health import health_check as new_health_check
import logging

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([AllowAny])
def legacy_process_request(request):
    """
    Legacy endpoint: /process_request/
    Redirects to new /calculations/ endpoint for backwards compatibility.
    """
    logger.info("Legacy process_request endpoint called, redirecting to new calculations endpoint")
    
    # Simply call the new process_request function
    return new_process_request(request)


@api_view(["GET"])
@permission_classes([AllowAny])
def legacy_health_check(request):
    """
    Legacy health check endpoint for backwards compatibility.
    """
    logger.info("Legacy health check endpoint called")
    
    # Call the new health check function
    return new_health_check(request)
