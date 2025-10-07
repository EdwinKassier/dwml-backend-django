"""Portfolio-related views for cryptocurrency calculations."""

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from api.models.portfolio import Results, LOGGING
from api.models.portfolio import ResultsSerializer, LOGGINGSerializer
from api.serializers.portfolio import CalculationRequestSerializer
from api.services.portfolio_service import PortfolioService
import logging

logger = logging.getLogger(__name__)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def result_list(request):
    """
    List all results, or create a new main result.
    """
    logger.debug(f"Request received: {request.method} {request.path}")
    
    if request.method == 'GET':
        results = Results.objects.all()
        serializer = ResultsSerializer(results, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ResultsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
@permission_classes([AllowAny])
def result_detail(request, query):
    """
    Retrieve, update or delete a main result.
    """
    try:
        result = Results.objects.get(QUERY=query)
    except Results.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ResultsSerializer(result)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ResultsSerializer(result, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def log_list(request):
    """
    List all logs, or create a new log entry.
    """
    if request.method == 'GET':
        logs = LOGGING.objects.all()
        serializer = LOGGINGSerializer(logs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LOGGINGSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
@permission_classes([AllowAny])
def log_detail(request, symbol):
    """
    Retrieve, update or delete a log entry.
    """
    try:
        log = LOGGING.objects.get(SYMBOL=symbol)
    except LOGGING.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LOGGINGSerializer(log)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LOGGINGSerializer(log, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def process_request(request):
    """
    Process cryptocurrency calculation request.
    """
    try:
        # Validate input parameters
        serializer = CalculationRequestSerializer(data=request.GET)
        if not serializer.is_valid():
            return Response({
                'error': 'Invalid input parameters',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        symbol = serializer.validated_data['symbol']
        investment = serializer.validated_data['investment']

        logger.info(f"Processing calculation request for {symbol} with investment ${investment}")

        # Use service layer for business logic
        portfolio_service = PortfolioService()
        result = portfolio_service.calculate_portfolio_value(symbol, investment)

        if result['success']:
            return Response({
                'success': True,
                'data': result['data']
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.exception(f"Error processing request: {str(e)}")
        return Response({
            'success': False,
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
