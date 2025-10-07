"""Health check views for system monitoring."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import datetime


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for deployment verification."""
    return Response(
        {
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "service": "Crypto API",
        }
    )
