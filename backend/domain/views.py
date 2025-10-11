"""Domain views - all API endpoints in one place."""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import (
    CalculationRequestSerializer,
    ErrorResponseSerializer,
    MarketPriceSerializer,
    OpeningAverageSerializer,
    PortfolioLogSerializer,
    PortfolioResultSerializer,
    PriceRequestSerializer,
)
from .services import AnalyticsService, MarketDataService, PortfolioService

# ============================================================================
# PORTFOLIO ENDPOINTS (including main process_request)
# ============================================================================


@extend_schema(
    request=CalculationRequestSerializer,
    responses={200: PortfolioResultSerializer, 400: ErrorResponseSerializer},
)
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def process_request(request):
    """
    Main DWML endpoint - calculate portfolio value.

    Supports both GET (for backwards compatibility) and POST.
    This is the core endpoint of the application.
    """
    # Support both GET and POST
    data = request.GET if request.method == "GET" else request.data

    # Deserialize and validate input
    serializer = CalculationRequestSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    # Execute business logic
    service = PortfolioService()
    result = service.process_request(
        symbol=serializer.validated_data["symbol"],
        investment=serializer.validated_data["investment"],
    )

    # Serialize and return response
    response_serializer = PortfolioResultSerializer(result)
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(responses={200: PortfolioResultSerializer(many=True)})
@api_view(["GET"])
@permission_classes([AllowAny])
def result_list(request):
    """List portfolio calculation results."""
    symbol = request.query_params.get("symbol")
    limit = int(request.query_params.get("limit", 100))

    service = PortfolioService()
    results = service.get_results(symbol=symbol, limit=limit)

    serializer = PortfolioResultSerializer(results, many=True)
    return Response(serializer.data)


@extend_schema(responses={200: PortfolioResultSerializer})
@api_view(["GET"])
@permission_classes([AllowAny])
def result_detail(request, result_id: int):
    """Get specific portfolio result."""
    service = PortfolioService()
    result = service.get_result(result_id)

    serializer = PortfolioResultSerializer(result)
    return Response(serializer.data)


@extend_schema(responses={200: PortfolioLogSerializer(many=True)})
@api_view(["GET"])
@permission_classes([AllowAny])
def log_list(request):
    """List portfolio audit logs."""
    from .models import PortfolioLog

    symbol = request.query_params.get("symbol")
    queryset = PortfolioLog.objects.all()

    if symbol:
        queryset = queryset.filter(symbol=symbol.upper())

    logs = list(queryset[:100])
    serializer = PortfolioLogSerializer(logs, many=True)
    return Response(serializer.data)


# ============================================================================
# MARKET DATA ENDPOINTS
# ============================================================================


@extend_schema(
    parameters=[PriceRequestSerializer],
    responses={200: MarketPriceSerializer},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def current_price(request):
    """Get current price for a cryptocurrency."""
    serializer = PriceRequestSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    symbol = serializer.validated_data["symbol"]
    service = MarketDataService()
    price = service.get_current_price(symbol)

    return Response({"symbol": symbol.upper(), "price": float(price)})


@extend_schema(
    parameters=[PriceRequestSerializer],
    responses={200: OpeningAverageSerializer},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def opening_average(request):
    """Get opening average price for a cryptocurrency."""
    serializer = PriceRequestSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    symbol = serializer.validated_data["symbol"]
    service = MarketDataService()
    average = service.get_opening_average(symbol)

    return Response({"symbol": symbol.upper(), "average": float(average)})


@extend_schema(responses={200: MarketPriceSerializer(many=True)})
@api_view(["GET"])
@permission_classes([AllowAny])
def price_history(request):
    """Get price history for a cryptocurrency."""
    symbol = request.query_params.get("symbol", "BTC")
    limit = int(request.query_params.get("limit", 100))

    service = MarketDataService()
    history = service.get_price_history(symbol, limit=limit)

    serializer = MarketPriceSerializer(history, many=True)
    return Response(serializer.data)


# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================


@extend_schema(responses={200: dict})
@api_view(["GET"])
@permission_classes([AllowAny])
def covid_prediction(request):
    """Get COVID-19 impact prediction."""
    service = AnalyticsService()
    prediction = service.get_covid_prediction()
    return Response(prediction)


@extend_schema(responses={200: dict})
@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_report(request):
    """Generate analytics report."""
    symbol = request.query_params.get("symbol")

    service = AnalyticsService()
    report = service.generate_report(symbol=symbol)
    return Response(report)


# ============================================================================
# HEALTH CHECK
# ============================================================================


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for load balancers."""
    return Response(
        {
            "status": "healthy",
            "service": "dwml-backend",
            "version": "2.0.0",
        }
    )
