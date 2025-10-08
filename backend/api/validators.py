"""Custom validators for the API."""

import re
from decimal import Decimal

from django.core.exceptions import ValidationError
from rest_framework import serializers


class CryptocurrencySymbolValidator:
    """Validator for cryptocurrency symbols."""

    def __call__(self, value):
        if not re.match(r"^[A-Z0-9]{2,10}$", value.upper()):
            raise ValidationError(
                "Symbol must contain only letters and numbers, 2-10 characters"
            )
        return value.upper()


class InvestmentAmountValidator:
    """Validator for investment amounts."""

    def __call__(self, value):
        if value <= 0:
            raise ValidationError("Investment must be greater than zero")
        if value > Decimal("1000000.00"):
            raise ValidationError("Investment cannot exceed $1,000,000")
        return value


class PriceValidator:
    """Validator for price values."""

    def __call__(self, value):
        if value < 0:
            raise ValidationError("Price cannot be negative")
        if value > Decimal("999999999.99"):
            raise ValidationError("Price exceeds maximum allowed value")
        return value


class DateRangeValidator:
    """Validator for date ranges."""

    def __init__(self, max_days=365):
        self.max_days = max_days

    def __call__(self, value):
        from datetime import datetime, timedelta

        if isinstance(value, dict):
            start_date = value.get("start_date")
            end_date = value.get("end_date")

            if start_date and end_date:
                if end_date < start_date:
                    raise ValidationError("End date must be after start date")

                if (end_date - start_date).days > self.max_days:
                    raise ValidationError(
                        f"Date range cannot exceed {self.max_days} days"
                    )

        return value


class RateLimitValidator:
    """Validator for rate limiting."""

    def __init__(self, max_requests=100, window_minutes=60):
        self.max_requests = max_requests
        self.window_minutes = window_minutes

    def __call__(self, request):
        # This would integrate with a rate limiting service like Redis
        # For now, it's a placeholder
        return True
