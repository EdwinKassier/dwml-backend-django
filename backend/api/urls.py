"""URL configuration for the API app with versioning."""

from django.urls import include, path

from .views import analytics, health, market_data, portfolio

app_name = "api"

# API v1 URLs
urlpatterns = [
    # Health endpoints
    path("health/", health.health_check, name="health-check"),
    # Portfolio endpoints
    path("results/", portfolio.result_list, name="result-list"),
    path("results/<str:query>/", portfolio.result_detail, name="result-detail"),
    path("logs/", portfolio.log_list, name="log-list"),
    path("logs/<str:symbol>/", portfolio.log_detail, name="log-detail"),
    path("calculations/", portfolio.process_request, name="calculation-create"),
    # Market data endpoints
    path(
        "opening-averages/",
        market_data.opening_average_list,
        name="opening-average-list",
    ),
    path(
        "opening-averages/<str:symbol>/",
        market_data.opening_average_detail,
        name="opening-average-detail",
    ),
    # Analytics endpoints
    path("predictions/covid/", analytics.covid_prediction, name="covid-prediction"),
    # Backwards compatibility endpoints
    path("process_request/", portfolio.process_request, name="process-request-legacy"),
]
