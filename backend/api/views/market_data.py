"""Market data views for cryptocurrency market information."""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from api.models.market_data import OpeningAverage
from api.models.market_data import OpeningAverageSerializer
import logging

logger = logging.getLogger(__name__)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def opening_average_list(request):
    """
    List all opening averages, or create a new opening average.
    """
    if request.method == 'GET':
        averages = OpeningAverage.objects.all()
        serializer = OpeningAverageSerializer(averages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OpeningAverageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
@permission_classes([AllowAny])
def opening_average_detail(request, symbol):
    """
    Retrieve, update or delete an opening average.
    """
    try:
        average = OpeningAverage.objects.get(SYMBOL=symbol)
    except OpeningAverage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OpeningAverageSerializer(average)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OpeningAverageSerializer(average, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        average.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
