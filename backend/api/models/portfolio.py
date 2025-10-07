"""Portfolio-related models."""

from django.db import models
from rest_framework import serializers


class Results(models.Model):
    """Model for storing portfolio calculation results."""
    QUERY = models.CharField(max_length=100)
    NUMBERCOINS = models.FloatField()
    PROFIT = models.FloatField()
    GROWTHFACTOR = models.FloatField()
    LAMBOS = models.FloatField()
    INVESTMENT = models.FloatField()
    SYMBOL = models.CharField(max_length=100)
    GENERATIONDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'results'
        ordering = ['-GENERATIONDATE']

    def __str__(self):
        return f"{self.SYMBOL} - {self.QUERY}"


class LOGGING(models.Model):
    """Model for storing portfolio calculation logs."""
    SYMBOL = models.CharField(max_length=100)
    INVESTMENT = models.FloatField()
    GENERATIONDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'logging'
        ordering = ['-GENERATIONDATE']

    def __str__(self):
        return f"{self.SYMBOL} - ${self.INVESTMENT}"


class ResultsSerializer(serializers.ModelSerializer):
    """Serializer for Results model."""
    class Meta:
        model = Results
        fields = '__all__'


class LOGGINGSerializer(serializers.ModelSerializer):
    """Serializer for LOGGING model."""
    class Meta:
        model = LOGGING
        fields = '__all__'
