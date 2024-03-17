from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from datetime import datetime
from rest_framework import serializers
from django.db import models

# Create your models here.


class Results(models.Model):
    QUERY = models.CharField(max_length=100)
    NUMBERCOINS = models.FloatField()
    PROFIT = models.FloatField()
    GROWTHFACTOR = models.FloatField()
    LAMBOS = models.FloatField()
    INVESTMENT = models.FloatField()
    SYMBOL = models.CharField(max_length=100)
    GENERATIONDATE = models.DateTimeField(auto_now_add=True)

class ResultsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Results
        fields = '__all__'


class OPENING_AVERAGE(models.Model):
    SYMBOL = models.CharField(max_length=100)
    AVERAGE = models.FloatField()
    GENERATIONDATE = models.DateTimeField(auto_now_add=True)

class OPENING_AVERAGESerializer(serializers.ModelSerializer):

    class Meta:
        model = OPENING_AVERAGE
        fields = '__all__'


class LOGGING(models.Model):
    SYMBOL = models.CharField(max_length=100)
    INVESTMENT = models.FloatField()
    GENERATIONDATE = models.DateTimeField(auto_now_add=True)

class LOGGINGSerializer(serializers.ModelSerializer):

    class Meta:
        model = LOGGING
        fields = '__all__'

