"""Market data serializers."""

from api.models.market_data import OpeningAverage
from rest_framework import serializers


class MarketPriceSerializer(serializers.Serializer):
    """Serializer for market price data."""

    symbol = serializers.CharField(max_length=10)
    price = serializers.DecimalField(max_digits=20, decimal_places=8)
    source = serializers.CharField(max_length=20)
    timestamp = serializers.DateTimeField()


class MarketSummarySerializer(serializers.Serializer):
    """Serializer for market summary data."""

    summary = serializers.DictField()
    total_symbols = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
