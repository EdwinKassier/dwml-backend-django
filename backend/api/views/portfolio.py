"""Portfolio-related views for cryptocurrency calculations."""

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers
from api.models.portfolio import PortfolioResult, PortfolioLog
from api.models.portfolio import PortfolioResultSerializer, PortfolioLogSerializer
from api.serializers.portfolio import CalculationRequestSerializer
from api.services.portfolio_service import PortfolioService
from api.pagination import StandardResultsSetPagination
from api.permissions import IsAdminOrReadOnly
from api.validators import CryptocurrencySymbolValidator, InvestmentAmountValidator
from django.core.paginator import Paginator
import logging

logger = logging.getLogger(__name__)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def result_list(request):
    """
    List all results, or create a new main result.
    """
    logger.debug(f"Request received: {request.method} {request.path}")
    
    if request.method == 'GET':
        # Add pagination
        paginator = StandardResultsSetPagination()
        results = PortfolioResult.objects.all().order_by('-generation_date')
        page = paginator.paginate_queryset(results, request)
        
        if page is not None:
            serializer = PortfolioResultSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = PortfolioResultSerializer(results, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PortfolioResultSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def result_detail(request, query):
    """
    Retrieve, update or delete a main result.
    """
    try:
        result = PortfolioResult.objects.get(query=query)
    except PortfolioResult.DoesNotExist:
        return Response({
            'error': 'Result not found',
            'query': query
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PortfolioResultSerializer(result)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PortfolioResultSerializer(result, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def log_list(request):
    """
    List all logs, or create a new log entry.
    """
    if request.method == 'GET':
        # Add pagination
        paginator = StandardResultsSetPagination()
        logs = PortfolioLog.objects.all().order_by('-generation_date')
        page = paginator.paginate_queryset(logs, request)
        
        if page is not None:
            serializer = PortfolioLogSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = PortfolioLogSerializer(logs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PortfolioLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def log_detail(request, symbol):
    """
    Retrieve, update or delete a log entry.
    """
    try:
        log = PortfolioLog.objects.get(symbol=symbol)
    except PortfolioLog.DoesNotExist:
        return Response({
            'error': 'Log entry not found',
            'symbol': symbol
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PortfolioLogSerializer(log)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PortfolioLogSerializer(log, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def process_request(request):
    """
    Process cryptocurrency calculation request with enhanced validation.
    """
    try:
        # Validate input parameters with custom validators
        serializer = CalculationRequestSerializer(data=request.GET)
        if not serializer.is_valid():
            return Response({
                'error': 'Invalid input parameters',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        symbol = serializer.validated_data['symbol']
        investment = serializer.validated_data['investment']

        # Additional validation
        symbol_validator = CryptocurrencySymbolValidator()
        investment_validator = InvestmentAmountValidator()
        
        try:
            symbol = symbol_validator(symbol)
            investment = investment_validator(investment)
        except Exception as e:
            return Response({
                'error': 'Validation failed',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

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