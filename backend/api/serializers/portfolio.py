"""Portfolio-related serializers."""

from rest_framework import serializers
from api.models.portfolio import Results, LOGGING
from api.models.portfolio import ResultsSerializer, LOGGINGSerializer
import re


class CalculationRequestSerializer(serializers.Serializer):
    """Serializer for calculation request validation."""
    symbol = serializers.CharField(
        max_length=10,
        min_length=2,
        required=True,
        help_text="Cryptocurrency symbol (e.g., BTC, ETH)"
    )
    investment = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        max_value=1000000.00,
        required=True,
        help_text="Investment amount in USD"
    )
    
    def validate_symbol(self, value):
        """Validate cryptocurrency symbol format."""
        if not re.match(r'^[A-Z0-9]+$', value.upper()):
            raise serializers.ValidationError(
                "Symbol must contain only letters and numbers"
            )
        return value.upper()
    
    def validate_investment(self, value):
        """Validate investment amount."""
        if value <= 0:
            raise serializers.ValidationError(
                "Investment must be greater than zero"
            )
        if value > 1000000:
            raise serializers.ValidationError(
                "Investment cannot exceed $1,000,000"
            )
        return value


class PortfolioResultSerializer(serializers.Serializer):
    """Serializer for portfolio calculation results."""
    symbol = serializers.CharField(max_length=10)
    investment = serializers.DecimalField(max_digits=12, decimal_places=2)
    current_price = serializers.DecimalField(max_digits=20, decimal_places=8)
    coins_purchased = serializers.DecimalField(max_digits=20, decimal_places=8)
    total_value = serializers.DecimalField(max_digits=20, decimal_places=2)
    profit = serializers.DecimalField(max_digits=20, decimal_places=2)
    growth_factor = serializers.DecimalField(max_digits=10, decimal_places=4)
    roi_percentage = serializers.DecimalField(max_digits=10, decimal_places=2)
