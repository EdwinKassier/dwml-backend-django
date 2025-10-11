"""Domain services - all business logic in one place."""

import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional

import requests
from django.core.cache import cache
from django.db import transaction
from shared.exceptions.custom_exceptions import (
    ExternalServiceError,
    NotFoundError,
    ValidationError,
)

from .models import (
    AnalysisReport,
    MarketPrice,
    OpeningAverage,
    PortfolioLog,
    PortfolioResult,
    Prediction,
)

logger = logging.getLogger(__name__)


class KrakenClient:
    """
    Client for Kraken cryptocurrency exchange API.
    Isolates external API dependency.
    """

    BASE_URL = "https://api.kraken.com/0/public"
    TIMEOUT = 30

    def get_historical_ohlc(
        self, symbol: str, days: int = 30, interval: int = 21600  # 6 hours
    ) -> Optional[List[Dict]]:
        """Get historical OHLC data."""
        try:
            # Calculate timestamp
            since = int((datetime.now() - timedelta(days=days)).timestamp())

            url = f"{self.BASE_URL}/OHLC"
            params = {"pair": f"{symbol}USD", "interval": interval, "since": since}

            response = requests.get(url, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()

            data = response.json()

            if "error" in data and data["error"]:
                logger.error("Kraken API error: %s", data["error"])
                return None

            if "result" not in data:
                return None

            # Parse OHLC data
            result_keys = [k for k in data["result"].keys() if not k.startswith("last")]
            if not result_keys:
                return None

            ohlc_key = result_keys[0]
            ohlc_data = data["result"][ohlc_key]

            parsed = []
            for candle in ohlc_data:
                parsed.append(
                    {
                        "timestamp": candle[0],
                        "open": float(candle[1]),
                        "high": float(candle[2]),
                        "low": float(candle[3]),
                        "close": float(candle[4]),
                        "volume": float(candle[6]),
                    }
                )

            return parsed

        except requests.RequestException as e:
            logger.error("Kraken API request failed: %s", str(e))
            return None
        except Exception as e:
            logger.error("Error parsing Kraken response: %s", str(e))
            return None

    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for symbol."""
        try:
            # Use recent OHLC data
            data = self.get_historical_ohlc(symbol, days=1)
            if not data:
                return None

            # Get most recent close price
            return data[-1]["close"]

        except Exception as e:
            logger.error("Error getting current price: %s", str(e))
            return None

    def symbol_exists(self, symbol: str) -> bool:
        """Check if symbol exists on exchange."""
        data = self.get_historical_ohlc(symbol, days=1)
        return data is not None and len(data) > 0


class MarketDataService:
    """Service for fetching and managing market data."""

    CACHE_TTL_OPENING = 3600  # 1 hour for historical data
    CACHE_TTL_CURRENT = 60  # 1 minute for current prices

    def __init__(self, client: Optional[KrakenClient] = None):
        self.client = client or KrakenClient()

    def get_opening_average(self, symbol: str) -> Optional[Decimal]:
        """
        Get opening average price (cached).

        Uses cache-aside pattern:
        1. Check cache
        2. Check database
        3. Fetch from API
        4. Store in DB and cache
        """
        symbol = symbol.upper()
        cache_key = f"opening_avg:{symbol}"

        # Try cache
        cached = cache.get(cache_key)
        if cached is not None:
            logger.debug("Cache hit: opening average for %s", symbol)
            return Decimal(str(cached))

        # Try database
        try:
            obj = OpeningAverage.objects.filter(symbol=symbol).latest("created_at")
            cache.set(cache_key, str(obj.average), self.CACHE_TTL_OPENING)
            return obj.average

        except OpeningAverage.DoesNotExist:
            pass

        # Fetch from API
        logger.info("Fetching opening average from API: %s", symbol)

        try:
            data = self.client.get_historical_ohlc(symbol, days=30)
            if not data or len(data) < 4:
                logger.warning("Insufficient data for %s", symbol)
                return None

            # Calculate average from first month (4 data points)
            opening_prices = [Decimal(str(d["close"])) for d in data[:4]]
            average = sum(opening_prices) / len(opening_prices)

            # Store in database
            OpeningAverage.objects.create(symbol=symbol, average=average)

            # Cache it
            cache.set(cache_key, str(average), self.CACHE_TTL_OPENING)

            return average

        except Exception as e:
            logger.error("Error fetching opening average: %s", e)
            raise ExternalServiceError(f"Failed to get opening average for {symbol}")

    def get_current_price(self, symbol: str) -> Optional[Decimal]:
        """Get current price (cached with shorter TTL)."""
        symbol = symbol.upper()
        cache_key = f"current_price:{symbol}"

        # Try cache
        cached = cache.get(cache_key)
        if cached is not None:
            logger.debug("Cache hit: current price for %s", symbol)
            return Decimal(str(cached))

        # Fetch from API
        try:
            price = self.client.get_current_price(symbol)
            if price is None:
                logger.warning("No current price for %s", symbol)
                return None

            price_decimal = Decimal(str(price))

            # Store snapshot in database
            MarketPrice.objects.create(symbol=symbol, price=price_decimal)

            # Cache it
            cache.set(cache_key, str(price_decimal), self.CACHE_TTL_CURRENT)

            return price_decimal

        except Exception as e:
            logger.error("Error fetching current price: %s", e)
            raise ExternalServiceError(f"Failed to get current price for {symbol}")

    def get_price_history(self, symbol: str, limit: int = 100) -> List[MarketPrice]:
        """Get historical price snapshots."""
        return list(
            MarketPrice.objects.filter(symbol=symbol.upper()).order_by("-timestamp")[
                :limit
            ]
        )


class PortfolioCalculator:
    """
    Domain service for portfolio calculations.
    Pure business logic - no dependencies on infrastructure.
    """

    LAMBO_PRICE = Decimal("200000")
    MIN_INVESTMENT = Decimal("0.01")
    MAX_INVESTMENT = Decimal("1000000")

    def validate_investment(self, investment: Decimal) -> None:
        """Validate investment amount."""
        if investment < self.MIN_INVESTMENT:
            raise ValidationError(f"Investment must be at least ${self.MIN_INVESTMENT}")
        if investment > self.MAX_INVESTMENT:
            raise ValidationError(f"Investment cannot exceed ${self.MAX_INVESTMENT}")

    def calculate(
        self, investment: Decimal, opening_price: Decimal, current_price: Decimal
    ) -> Dict[str, Decimal]:
        """
        Calculate portfolio metrics.

        Returns dict with calculation results (not a model).
        """
        # Validate inputs
        self.validate_investment(investment)

        if opening_price <= 0:
            raise ValidationError("Opening price must be positive")
        if current_price <= 0:
            raise ValidationError("Current price must be positive")

        # Business logic calculations
        number_coins = investment / opening_price
        current_value = number_coins * current_price
        profit = current_value - investment
        growth_factor = (current_value / investment) - 1
        lambos = profit / self.LAMBO_PRICE if profit > 0 else Decimal("0")

        return {
            "number_coins": number_coins,
            "profit": profit,
            "growth_factor": growth_factor,
            "lambos": lambos,
        }


class PortfolioService:
    """
    Main portfolio service - orchestrates portfolio calculations.
    This is the primary service for the process_request endpoint.
    """

    def __init__(
        self,
        market_service: Optional[MarketDataService] = None,
        calculator: Optional[PortfolioCalculator] = None,
    ):
        """Initialize with dependencies."""
        self.market_service = market_service or MarketDataService()
        self.calculator = calculator or PortfolioCalculator()

    @transaction.atomic
    def process_request(self, symbol: str, investment: Decimal) -> PortfolioResult:
        """
        Main DWML endpoint logic - calculate portfolio value.

        This is the core business operation that:
        1. Validates input
        2. Fetches market data
        3. Calculates portfolio metrics
        4. Saves results
        5. Logs the operation

        Raises:
            ValidationError: Invalid input
            NotFoundError: Price data not available

        Returns:
            PortfolioResult: The calculated result
        """
        # Normalize symbol
        symbol = symbol.upper().strip()

        # Log operation
        self._create_log(
            symbol,
            "process_request_started",
            "INFO",
            {"investment": str(investment)},
        )

        try:
            # Get price data
            opening_price = self.market_service.get_opening_average(symbol)
            current_price = self.market_service.get_current_price(symbol)

            if opening_price is None or current_price is None:
                raise NotFoundError(f"Price data not available for {symbol}")

            # Calculate using domain service
            metrics = self.calculator.calculate(
                investment=investment,
                opening_price=opening_price,
                current_price=current_price,
            )

            # Create result entity
            result = PortfolioResult.objects.create(
                symbol=symbol, investment=investment, **metrics
            )

            # Log success
            self._create_log(
                symbol,
                "process_request_completed",
                "INFO",
                {"result_id": str(result.id), "profit": str(result.profit)},
            )

            logger.info(
                "Portfolio calculated: %s - Profit: $%.2f (%.1f%%)",
                symbol,
                result.profit,
                result.roi_percentage,
            )

            return result

        except (ValidationError, NotFoundError):
            # Log and re-raise domain exceptions
            raise
        except Exception as e:
            # Log unexpected errors
            self._create_log(
                symbol,
                "process_request_error",
                "ERROR",
                {"error": str(e)},
            )
            logger.exception("Unexpected error processing request: %s", symbol)
            raise

    def get_results(
        self, symbol: Optional[str] = None, limit: int = 100
    ) -> List[PortfolioResult]:
        """Get portfolio results."""
        queryset = PortfolioResult.objects.all()

        if symbol:
            queryset = queryset.filter(symbol=symbol.upper())

        return list(queryset[:limit])

    def get_result(self, result_id: int) -> PortfolioResult:
        """Get specific portfolio result."""
        try:
            return PortfolioResult.objects.get(id=result_id)
        except PortfolioResult.DoesNotExist:
            raise NotFoundError(f"Portfolio result {result_id} not found")

    def _create_log(
        self, symbol: str, action: str, level: str, metadata: Dict[str, Any]
    ) -> None:
        """Internal helper to create audit log."""
        try:
            PortfolioLog.objects.create(
                symbol=symbol, action=action, level=level, metadata=metadata
            )
        except Exception as e:
            logger.error("Failed to create log: %s", e)


class CovidAnalyzer:
    """Domain service for COVID-19 impact analysis."""

    def analyze_impact(self, covid_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze COVID-19 impact on cryptocurrency markets."""
        try:
            cases = covid_data.get("cases", 0)
            deaths = covid_data.get("deaths", 0)

            # Calculate severity score (normalized)
            severity_score = (cases * 0.7 + deaths * 0.3) / 1000000

            # Determine market impact
            if severity_score > 0.5:
                market_impact = "HIGH"
            elif severity_score > 0.2:
                market_impact = "MEDIUM"
            else:
                market_impact = "LOW"

            # Generate recommendation
            recommendation = self._get_recommendation(severity_score)

            return {
                "severity_score": round(severity_score, 2),
                "market_impact": market_impact,
                "recommendation": recommendation,
                "confidence": min(severity_score * 100, 95),
            }

        except Exception as e:
            logger.error("Error analyzing COVID impact: %s", str(e))
            return {
                "severity_score": 0,
                "market_impact": "UNKNOWN",
                "recommendation": "Unable to analyze",
                "confidence": 0,
            }

    def _get_recommendation(self, severity_score: float) -> str:
        """Get market recommendation based on severity score."""
        if severity_score > 0.7:
            return "Consider reducing crypto exposure due to high COVID impact"
        elif severity_score > 0.4:
            return "Monitor market conditions closely, moderate COVID impact"
        else:
            return "Low COVID impact, normal market conditions expected"


class AnalyticsService:
    """Service for analytics operations."""

    def __init__(self, covid_analyzer: Optional[CovidAnalyzer] = None):
        self.covid_analyzer = covid_analyzer or CovidAnalyzer()

    def get_covid_prediction(self) -> Dict[str, Any]:
        """Get COVID-19 impact prediction."""
        try:
            # Mock data for now
            mock_covid_data = {
                "cases": 1000000,
                "deaths": 50000,
                "timestamp": "2025-10-11T00:00:00Z",
            }

            analysis = self.covid_analyzer.analyze_impact(mock_covid_data)

            # Store prediction
            Prediction.objects.create(
                prediction_type="covid_impact",
                prediction_data={**mock_covid_data, **analysis},
                confidence=Decimal(str(analysis["confidence"])),
            )

            return {
                "covid_data": mock_covid_data,
                "analysis": analysis,
                "timestamp": mock_covid_data["timestamp"],
                "source": "covid_analyzer",
            }

        except Exception as e:
            logger.exception("Error getting COVID prediction: %s", str(e))
            raise ExternalServiceError("Failed to generate COVID prediction")

    def generate_report(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Generate analytics report."""
        try:
            report_data = {
                "symbol": symbol,
                "charts": [],
                "metrics": {},
                "recommendations": [],
            }

            report = AnalysisReport.objects.create(
                report_type="market_analysis",
                data=report_data,
                summary=f"Analytics report for {symbol or 'market'}",
            )

            return {
                "id": report.id,
                "report_type": report.report_type,
                "data": report_data,
                "summary": report.summary,
                "created_at": report.created_at.isoformat(),
            }

        except Exception as e:
            logger.exception("Error generating report: %s", str(e))
            raise
