from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from api.models import Results
from api.models import ResultsSerializer
import logging

# Create your views here.


@csrf_exempt
@api_view(["GET", "POST"])
def result_list(request):
    """
    List all results, or create a new result.
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
    Retrieve, update or delete a result.
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