from django.contrib import admin
from django.urls import path, include                 # add this
from rest_framework import routers                    # add this
from api.api_views import result_list, result_detail, opening_average_list, opening_average_detail,log_list,log_detail,process_request


urlpatterns = [
    path('results/',result_list,name='result_list' ),
    path('aux_result/<str:query>',result_detail, name = 'result_detail'),
    path('opening_averages/',opening_average_list, name = 'opening_average_list'),
    path('aux_opening_averages/<str:symbol>',opening_average_detail, name = 'opening_average_detail'),
    path('logging/',log_list, name = 'log_list'),
    path('aux_logging/<str:symbol>',log_detail, name = 'log_detail'),

    path('process_request/',process_request, name = 'process_request'),      
]