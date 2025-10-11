"""Domain URL configuration."""

from django.urls import path

from . import views

app_name = "domain"

urlpatterns = [
    # Main DWML endpoint
    path("process_request/", views.process_request, name="process-request"),
    # Portfolio results
    path("results/", views.result_list, name="result-list"),
    path("results/<int:result_id>/", views.result_detail, name="result-detail"),
    # Logs
    path("logs/", views.log_list, name="log-list"),
    # Market data
    path("price/current/", views.current_price, name="current-price"),
    path("price/opening/", views.opening_average, name="opening-average"),
    path("price/history/", views.price_history, name="price-history"),
    # Analytics
    path("analytics/covid/", views.covid_prediction, name="covid-prediction"),
    path("analytics/report/", views.analytics_report, name="analytics-report"),
    # Health check
    path("health/", views.health_check, name="health-check"),
]
