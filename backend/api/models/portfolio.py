"""Portfolio-related models."""

from django.db import models
from rest_framework import serializers


class PortfolioResult(models.Model):
    """Model for storing portfolio calculation results."""

    query = models.CharField(max_length=100, db_index=True)
    number_coins = models.FloatField()
    profit = models.FloatField()
    growth_factor = models.FloatField()
    lambos = models.FloatField()
    investment = models.FloatField()
    symbol = models.CharField(max_length=100, db_index=True)
    generation_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "portfolio_results"
        ordering = ["-generation_date"]
        indexes = [
            models.Index(fields=["symbol", "generation_date"]),
            models.Index(fields=["query"]),
        ]

    def __str__(self):
        return f"{self.symbol} - {self.query}"


class PortfolioLog(models.Model):
    """Model for storing portfolio calculation logs."""

    symbol = models.CharField(max_length=100, db_index=True)
    message = models.TextField()
    level = models.CharField(max_length=20)
    generation_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "portfolio_logs"
        ordering = ["-generation_date"]
        indexes = [
            models.Index(fields=["symbol", "generation_date"]),
        ]

    def __str__(self):
        return f"{self.symbol} - {self.level}"


class PortfolioResultSerializer(serializers.ModelSerializer):
    """Serializer for PortfolioResult model."""

    class Meta:
        model = PortfolioResult
        fields = "__all__"


class PortfolioLogSerializer(serializers.ModelSerializer):
    """Serializer for PortfolioLog model."""

    class Meta:
        model = PortfolioLog
        fields = "__all__"


# Backwards compatibility aliases
Results = PortfolioResult
LOGGING = PortfolioLog
ResultsSerializer = PortfolioResultSerializer
LOGGINGSerializer = PortfolioLogSerializer
