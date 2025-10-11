"""Domain admin configuration."""

from django.contrib import admin

from .models import (
    AnalysisReport,
    MarketPrice,
    OpeningAverage,
    PortfolioLog,
    PortfolioResult,
    Prediction,
)


@admin.register(PortfolioResult)
class PortfolioResultAdmin(admin.ModelAdmin):
    """Admin interface for Portfolio Results."""

    list_display = [
        "id",
        "symbol",
        "investment",
        "profit",
        "roi_percentage",
        "generation_date",
    ]
    list_filter = ["symbol", "generation_date"]
    search_fields = ["symbol"]
    readonly_fields = [
        "id",
        "generation_date",
        "roi_percentage",
        "is_profitable",
        "can_buy_lambo",
        "risk_level",
    ]
    ordering = ["-generation_date"]


@admin.register(PortfolioLog)
class PortfolioLogAdmin(admin.ModelAdmin):
    """Admin interface for Portfolio Logs."""

    list_display = ["id", "symbol", "action", "level", "created_at"]
    list_filter = ["level", "symbol", "created_at"]
    search_fields = ["symbol", "action"]
    readonly_fields = ["id", "created_at", "metadata"]
    ordering = ["-created_at"]


@admin.register(OpeningAverage)
class OpeningAverageAdmin(admin.ModelAdmin):
    """Admin interface for Opening Averages."""

    list_display = ["id", "symbol", "average", "created_at"]
    list_filter = ["symbol", "created_at"]
    search_fields = ["symbol"]
    readonly_fields = ["id", "created_at"]
    ordering = ["-created_at"]


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    """Admin interface for Market Prices."""

    list_display = ["id", "symbol", "price", "volume", "timestamp"]
    list_filter = ["symbol", "timestamp"]
    search_fields = ["symbol"]
    readonly_fields = ["id", "timestamp"]
    ordering = ["-timestamp"]


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    """Admin interface for Predictions."""

    list_display = ["id", "prediction_type", "confidence", "created_at"]
    list_filter = ["prediction_type", "created_at"]
    search_fields = ["prediction_type"]
    readonly_fields = ["id", "created_at", "prediction_data"]
    ordering = ["-created_at"]


@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    """Admin interface for Analysis Reports."""

    list_display = ["id", "report_type", "summary", "created_at"]
    list_filter = ["report_type", "created_at"]
    search_fields = ["report_type", "summary"]
    readonly_fields = ["id", "created_at", "data"]
    ordering = ["-created_at"]
