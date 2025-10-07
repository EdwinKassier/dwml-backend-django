"""Market data models."""

from django.db import models
from rest_framework import serializers


class OpeningAverage(models.Model):
    """Model for storing opening average prices."""
    symbol = models.CharField(max_length=100, db_index=True)
    average = models.FloatField()
    generation_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'opening_averages'
        ordering = ['-generation_date']
        indexes = [
            models.Index(fields=['symbol', 'generation_date']),
        ]

    def __str__(self):
        return f"{self.symbol} - ${self.average}"


class OpeningAverageSerializer(serializers.ModelSerializer):
    """Serializer for OpeningAverage model."""
    class Meta:
        model = OpeningAverage
        fields = '__all__'
