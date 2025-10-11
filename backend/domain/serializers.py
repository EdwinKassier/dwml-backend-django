"""Domain serializers - all API serialization in one place."""

from decimal import Decimal

from rest_framework import serializers

from .models import (
    AnalysisReport,
    MarketPrice,
    OpeningAverage,
    PortfolioLog,
    PortfolioResult,
    Prediction,
)


class CalculationRequestSerializer(serializers.Serializer):
    """Request serializer for portfolio calculation (process_request)."""

    symbol = serializers.CharField(
        max_length=10, min_length=2, help_text="Cryptocurrency symbol (e.g., BTC, ETH)"
    )
    investment = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01"),
        max_value=Decimal("1000000"),
        help_text="Investment amount in USD",
    )

    def validate_symbol(self, value: str) -> str:
        """Uppercase and validate symbol."""
        return value.upper().strip()


class PortfolioResultSerializer(serializers.ModelSerializer):
    """Response serializer for portfolio results."""

    roi_percentage = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    is_profitable = serializers.BooleanField(read_only=True)
    can_buy_lambo = serializers.BooleanField(read_only=True)
    risk_level = serializers.CharField(read_only=True)

    class Meta:
        model = PortfolioResult
        fields = [
            "id",
            "symbol",
            "investment",
            "number_coins",
            "profit",
            "growth_factor",
            "lambos",
            "roi_percentage",
            "is_profitable",
            "can_buy_lambo",
            "risk_level",
            "generation_date",
        ]
        read_only_fields = fields


class PortfolioLogSerializer(serializers.ModelSerializer):
    """Serializer for portfolio logs."""

    class Meta:
        model = PortfolioLog
        fields = ["id", "symbol", "action", "level", "metadata", "created_at"]
        read_only_fields = fields


class OpeningAverageSerializer(serializers.ModelSerializer):
    """Serializer for opening average prices."""

    class Meta:
        model = OpeningAverage
        fields = ["id", "symbol", "average", "created_at"]
        read_only_fields = fields


class MarketPriceSerializer(serializers.ModelSerializer):
    """Serializer for market prices."""

    class Meta:
        model = MarketPrice
        fields = ["id", "symbol", "price", "volume", "timestamp"]
        read_only_fields = fields


class PriceRequestSerializer(serializers.Serializer):
    """Request serializer for price lookup."""

    symbol = serializers.CharField(
        max_length=10, min_length=2, help_text="Cryptocurrency symbol"
    )

    def validate_symbol(self, value: str) -> str:
        """Uppercase and validate symbol."""
        return value.upper().strip()


class PredictionSerializer(serializers.ModelSerializer):
    """Serializer for predictions."""

    class Meta:
        model = Prediction
        fields = [
            "id",
            "symbol",
            "prediction_type",
            "prediction_data",
            "confidence",
            "created_at",
        ]
        read_only_fields = fields


class AnalysisReportSerializer(serializers.ModelSerializer):
    """Serializer for analysis reports."""

    class Meta:
        model = AnalysisReport
        fields = ["id", "report_type", "data", "summary", "created_at"]
        read_only_fields = fields


class ErrorResponseSerializer(serializers.Serializer):
    """Error response serializer."""

    error = serializers.CharField()
    code = serializers.CharField(required=False)
    details = serializers.DictField(required=False)
