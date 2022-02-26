from django.contrib import admin
from django.urls import path, include                 # add this
from rest_framework import routers                    # add this
from api.api_views import result_list, result_detail


urlpatterns = [
    path('results/',result_list,name='result_list' ),
    path('get_result/<str:query>',result_detail, name = 'result_detail'),      
]