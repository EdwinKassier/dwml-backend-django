"""Analytics views for cryptocurrency analysis and predictions."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.services.analytics_service import AnalyticsService
import logging

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([AllowAny])
def covid_prediction(request):
    """
    COVID-19 impact prediction endpoint.
    """
    try:
        logger.info("Processing COVID prediction request")
        
        # Use service layer for business logic
        analytics_service = AnalyticsService()
        result = analytics_service.get_covid_prediction()

        if result['success']:
            return Response({
                'success': True,
                'data': result['data']
            }, status=200)
        else:
            return Response({
                'success': False,
                'error': result['error']
            }, status=500)

    except Exception as e:
        logger.exception(f"Error in COVID prediction: {str(e)}")
        return Response({
            'success': False,
            'error': 'Internal server error'
        }, status=500)
