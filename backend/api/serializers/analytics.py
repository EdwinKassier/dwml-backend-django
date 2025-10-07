"""Analytics serializers."""

from rest_framework import serializers


class CovidPredictionSerializer(serializers.Serializer):
    """Serializer for COVID prediction data."""
    covid_data = serializers.DictField()
    analysis = serializers.DictField()
    timestamp = serializers.CharField()
    source = serializers.CharField()


class AnalyticsReportSerializer(serializers.Serializer):
    """Serializer for analytics reports."""
    symbol = serializers.CharField(max_length=10)
    report_type = serializers.CharField()
    charts = serializers.ListField()
    metrics = serializers.DictField()
    recommendations = serializers.ListField()
