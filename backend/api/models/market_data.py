"""Market data models."""

from django.db import models
from rest_framework import serializers


class OpeningAverage(models.Model):
    """Model for storing opening average prices."""
    SYMBOL = models.CharField(max_length=100)
    AVERAGE = models.FloatField()
    GENERATIONDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'opening_average'
        ordering = ['-GENERATIONDATE']

    def __str__(self):
        return f"{self.SYMBOL} - ${self.AVERAGE}"


class OpeningAverageSerializer(serializers.ModelSerializer):
    """Serializer for OpeningAverage model."""
    class Meta:
        model = OpeningAverage
        fields = '__all__'
