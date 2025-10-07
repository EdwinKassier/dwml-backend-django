from django.urls import path
from api.api_views import (
    result_list, result_detail, 
    opening_average_list, opening_average_detail,
    log_list, log_detail,
    process_request, covid_prediction, health_check
)

app_name = 'api'

urlpatterns = [
    # Health check
    path('health/', health_check, name='health-check'),
    
    # Results endpoints
    path('results/', result_list, name='result-list'),
    path('results/<str:query>/', result_detail, name='result-detail'),
    
    # Opening averages endpoints
    path('opening-averages/', opening_average_list, name='opening-average-list'),
    path('opening-averages/<str:symbol>/', opening_average_detail, name='opening-average-detail'),
    
    # Logging endpoints
    path('logs/', log_list, name='log-list'),
    path('logs/<str:symbol>/', log_detail, name='log-detail'),
    
    # Business logic endpoints
    path('calculations/', process_request, name='calculation-create'),
    path('predictions/covid/', covid_prediction, name='covid-prediction'),
]