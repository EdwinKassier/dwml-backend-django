"""Domain models - all business entities in one place."""

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class PortfolioResult(models.Model):
    """
    Portfolio calculation result (domain entity).

    Rich model with behavior, not just data.
    """

    # Core domain attributes
    symbol = models.CharField(max_length=10, db_index=True)
    investment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    number_coins = models.DecimalField(max_digits=20, decimal_places=8)
    profit = models.DecimalField(max_digits=20, decimal_places=2)
    growth_factor = models.DecimalField(max_digits=10, decimal_places=4)
    lambos = models.DecimalField(max_digits=10, decimal_places=2)
    generation_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "portfolio_results"
        ordering = ["-generation_date"]
        indexes = [
            models.Index(fields=["symbol", "generation_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.symbol}: {self.profit:+.2f} ({self.roi_percentage:.1f}%)"

    # Domain behaviors
    @property
    def roi_percentage(self) -> Decimal:
        """Return on investment percentage."""
        if self.investment == 0:
            return Decimal("0")
        return (self.profit / self.investment) * 100

    def is_profitable(self) -> bool:
        """Check if investment is profitable."""
        return self.profit > 0

    def can_buy_lambo(self) -> bool:
        """Check if profit can buy a Lamborghini."""
        return self.lambos >= 1

    def risk_level(self) -> str:
        """Calculate risk level based on growth factor."""
        if self.growth_factor > 2:
            return "HIGH"
        elif self.growth_factor > 0.5:
            return "MEDIUM"
        else:
            return "LOW"


class PortfolioLog(models.Model):
    """Audit log for portfolio operations."""

    symbol = models.CharField(max_length=10, db_index=True)
    action = models.CharField(max_length=100)
    level = models.CharField(
        max_length=10,
        choices=[("INFO", "Info"), ("WARN", "Warning"), ("ERROR", "Error")],
        default="INFO",
    )
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "portfolio_logs"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.symbol} - {self.action} ({self.level})"


class OpeningAverage(models.Model):
    """Historical opening average price for a cryptocurrency."""

    symbol = models.CharField(max_length=10, db_index=True)
    average = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        validators=[MinValueValidator(Decimal("0"))],
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "opening_averages"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["symbol", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.symbol}: ${self.average}"


class MarketPrice(models.Model):
    """Current market price snapshot."""

    symbol = models.CharField(max_length=10, db_index=True)
    price = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        validators=[MinValueValidator(Decimal("0"))],
    )
    volume = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "market_prices"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["symbol", "timestamp"]),
        ]

    def __str__(self) -> str:
        return f"{self.symbol}: ${self.price} @ {self.timestamp}"


class Prediction(models.Model):
    """Market prediction entity."""

    symbol = models.CharField(max_length=10, db_index=True, null=True, blank=True)
    prediction_type = models.CharField(max_length=50)
    prediction_data = models.JSONField(default=dict)
    confidence = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "predictions"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.prediction_type} - {self.confidence}%"


class AnalysisReport(models.Model):
    """Analysis report entity."""

    report_type = models.CharField(max_length=50)
    data = models.JSONField(default=dict)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "analysis_reports"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.report_type} - {self.created_at}"
