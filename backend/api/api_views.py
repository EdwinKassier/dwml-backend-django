from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from api.models import Results
from api.models import ResultsSerializer
from api.models import OPENING_AVERAGE
from api.models import OPENING_AVERAGESerializer
from api.models import LOGGING
from api.models import LOGGINGSerializer
import logging
import re
from datetime import datetime

import traceback

import json

from .utils.data_collector import DataCollector
from .utils.graph_creator import GraphCreator
from .utils.covid_scraper import CovidScraper

logger = logging.getLogger(__name__)


# Create views here

# Serializers for input validation
class CalculationRequestSerializer(serializers.Serializer):
    """Serializer for calculation request validation."""
    symbol = serializers.CharField(
        max_length=10,
        min_length=2,
        required=True,
        help_text="Cryptocurrency symbol (e.g., BTC, ETH)"
    )
    investment = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        max_value=1000000.00,
        required=True,
        help_text="Investment amount in USD"
    )
    
    def validate_symbol(self, value):
        """Validate cryptocurrency symbol format."""
        if not re.match(r'^[A-Z0-9]+$', value.upper()):
            raise serializers.ValidationError(
                "Symbol must contain only letters and numbers"
            )
        return value.upper()
    
    def validate_investment(self, value):
        """Validate investment amount."""
        if value <= 0:
            raise serializers.ValidationError(
                "Investment must be greater than zero"
            )
        if value > 1000000:
            raise serializers.ValidationError(
                "Investment cannot exceed $1,000,000"
            )
        return value


'''Views for main result related views'''

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


@api_view(["GET", "POST","DELETE"])
@permission_classes([AllowAny])
def result_detail(request,query):
    """
    Retrieve, update or delete a main result.
    """
    logging.debug(request)
    result = Results.objects.filter(QUERY=query)
    logging.debug(result)

    if request.method == 'GET':
        serializer = ResultsSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ResultsSerializer(result, data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        result.delete()
        return HttpResponse(status=204)



'''Views for opening average results'''

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def opening_average_list(request):
    """
    List all opening_averages, or create a new opening average entry.
    """
    logging.debug(request)
    if request.method == 'GET':
        results = OPENING_AVERAGE.objects.all()
        serializer = OPENING_AVERAGESerializer(results, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OPENING_AVERAGESerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(["GET", "POST","DELETE"])
@permission_classes([AllowAny])
def opening_average_detail(request,symbol=None):
    """
    Retrieve, update or delete an opening average entry.
    """
    if symbol != None:
        logging.debug(request)
        result = OPENING_AVERAGE.objects.filter(symbol=symbol)
        logging.debug(result)

    if request.method == 'GET':
        serializer = OPENING_AVERAGESerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = OPENING_AVERAGESerializer(result, data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        result.delete()
        return HttpResponse(status=204)



'''Views for logging of interactions'''

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def log_list(request):
    """
    List all logs for the systems interactions
    """
    logging.debug(request)
    if request.method == 'GET':
        results = LOGGING.objects.all()
        serializer = LOGGINGSerializer(results, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LOGGINGSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(["GET", "POST","DELETE"])
@permission_classes([AllowAny])
def log_detail(request,symbol=None):
    """
    Retrieve, update or delete a logging entry for a specific symbol
    """
    if symbol != None:
        logging.debug(request)
        result = LOGGING.objects.filter(symbol=symbol)
        logging.debug(result)

    if request.method == 'GET':
        serializer = LOGGINGSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LOGGINGSerializer(result, data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        result.delete()
        return HttpResponse(status=204)


@api_view(["GET"])
@permission_classes([AllowAny])
def process_request(request):
    """
    Handle cryptocurrency calculation request.
    
    Query Parameters:
        - symbol (str): Cryptocurrency symbol (2-10 chars)
        - investment (decimal): Investment amount in USD (0.01-1000000)
    
    Returns:
        JSON with calculation results or error message
    """
    # Validate input
    serializer = CalculationRequestSerializer(data=request.GET)
    
    if not serializer.is_valid():
        return Response(
            {
                'error': 'Invalid input',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        validated_data = serializer.validated_data
        symbol = validated_data['symbol']
        investment = float(validated_data['investment'])
        
        logger.info(f"Processing request: symbol={symbol}, investment={investment}")
        
        collector = DataCollector(symbol, investment)
        creator = GraphCreator(symbol)
        
        result = collector.driver_logic()
        graph_data = creator.driver_logic()
        
        if result == "Symbol doesn't exist":
            return Response(
                {
                    'error': 'Symbol not found',
                    'message': f'Cryptocurrency symbol {symbol} not found on exchange'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(
            {
                'success': True,
                'data': {
                    'calculation': result,
                    'graph_data': graph_data
                }
            },
            status=status.HTTP_200_OK
        )
        
    except ValueError as e:
        logger.error(f"Value error in calculation: {e}")
        return Response(
            {'error': 'Invalid value', 'message': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.exception(f"Unexpected error processing request")
        return Response(
            {'error': 'Internal server error', 'message': 'An unexpected error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for deployment verification."""
    return Response({
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "service": "Crypto API"
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def covid_prediction(request):
    """
    Handle COVID prediction request from the frontend
    """
    try:
        logger.info("COVID prediction request received")
        
        scraper = CovidScraper("south-africa", "2023-03-06", True)
        result = scraper.driver_logic()

        return Response({
            'success': True,
            'data': {
                'message': "success",
                'graph_data': result
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.exception("Error in COVID prediction")
        return Response({
            'error': 'Internal server error',
            'message': 'COVID prediction failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)