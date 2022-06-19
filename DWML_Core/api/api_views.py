from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from api.models import Results
from api.models import ResultsSerializer
from api.models import OPENING_AVERAGE
from api.models import OPENING_AVERAGESerializer
from api.models import LOGGING
from api.models import LOGGINGSerializer
import logging

from .utils.DataCollector import DataCollector

# Create views here

'''Views for main result related views'''

@csrf_exempt
@api_view(["GET", "POST"])
def result_list(request):
    """
    List all results, or create a new main result.
    """
    logging.debug(request)
    if request.method == 'GET':
        results = Results.objects.all()
        serializer = ResultsSerializer(results, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ResultsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(["GET", "POST","DELETE"])
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

@csrf_exempt
@api_view(["GET", "POST"])
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


@csrf_exempt
@api_view(["GET", "POST","DELETE"])
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

@csrf_exempt
@api_view(["GET", "POST"])
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


@csrf_exempt
@api_view(["GET", "POST","DELETE"])
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


@csrf_exempt
@api_view(["GET"])
def log_list(request):
    """
    Handle an incoming request from the frontend
    """
    try:
        symbol = request.GET['symbol']
        investment = int(request.args.get('investment'))

        dataCollector = DataCollector(symbol,investment)
        result = dataCollector.driver_logic()

        return JsonResponse(status=200)
    except:
        return JsonResponse(status=500)