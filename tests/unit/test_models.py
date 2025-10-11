"""Unit tests for Django models."""
import pytest
from django.test import TestCase
from domain.models import OpeningAverage, PortfolioLog, PortfolioResult


@pytest.mark.django_db
@pytest.mark.unit
class TestPortfolioResultModel:
    """Test cases for PortfolioResult model."""

    def test_create_result(self):
        """Test creating a PortfolioResult instance."""
        result = PortfolioResult.objects.create(
            number_coins=1.5,
            profit=50000.0,
            growth_factor=2.5,
            lambos=0.25,
            investment=10000.0,
            symbol="BTC",
        )
        assert result.symbol == "BTC"
        assert result.number_coins == 1.5
        assert result.profit == 50000.0
        assert result.id is not None

    def test_result_string_fields(self):
        """Test string field constraints."""
        result = PortfolioResult.objects.create(
            number_coins=10.0,
            profit=5000.0,
            growth_factor=1.5,
            lambos=0.025,
            investment=1000.0,
            symbol="ETH",
        )
        assert len(result.symbol) <= 10
        assert result.symbol == "ETH"


@pytest.mark.django_db
@pytest.mark.unit
class TestOpeningAverageModel:
    """Test cases for OpeningAverage model."""

    def test_create_opening_average(self):
        """Test creating an OpeningAverage instance."""
        avg = OpeningAverage.objects.create(symbol="BTC", average=45000.0)
        assert avg.symbol == "BTC"
        assert avg.average == 45000.0
        assert avg.created_at is not None


@pytest.mark.django_db
@pytest.mark.unit
class TestPortfolioLogModel:
    """Test cases for PortfolioLog model."""

    def test_create_logging_entry(self):
        """Test creating a PortfolioLog instance."""
        log = PortfolioLog.objects.create(
            symbol="ETH", action="portfolio_calculation_completed", level="INFO"
        )
        assert log.symbol == "ETH"
        assert log.action == "portfolio_calculation_completed"
        assert log.level == "INFO"
        assert log.created_at is not None
