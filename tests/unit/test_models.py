"""Unit tests for Django models."""
import pytest
from django.test import TestCase
from api.models.portfolio import PortfolioResult, PortfolioLog
from api.models.market_data import OpeningAverage


@pytest.mark.django_db
@pytest.mark.unit
class TestPortfolioResultModel:
    """Test cases for PortfolioResult model."""

    def test_create_result(self):
        """Test creating a PortfolioResult instance."""
        result = PortfolioResult.objects.create(
            query="BTC",
            number_coins=1.5,
            profit=50000.0,
            growth_factor=2.5,
            lambos=0.25,
            investment=10000.0,
            symbol="BTC"
        )
        assert result.symbol == "BTC"
        assert result.number_coins == 1.5
        assert result.profit == 50000.0
        assert result.id is not None

    def test_result_string_fields(self):
        """Test string field constraints."""
        result = PortfolioResult.objects.create(
            query="ETH",
            number_coins=10.0,
            profit=5000.0,
            growth_factor=1.5,
            lambos=0.025,
            investment=1000.0,
            symbol="ETH"
        )
        assert len(result.symbol) <= 100
        assert len(result.query) <= 100


@pytest.mark.django_db
@pytest.mark.unit
class TestOpeningAverageModel:
    """Test cases for OpeningAverage model."""

    def test_create_opening_average(self):
        """Test creating an OpeningAverage instance."""
        avg = OpeningAverage.objects.create(
            symbol="BTC",
            average=45000.0
        )
        assert avg.symbol == "BTC"
        assert avg.average == 45000.0
        assert avg.generation_date is not None


@pytest.mark.django_db
@pytest.mark.unit
class TestPortfolioLogModel:
    """Test cases for PortfolioLog model."""

    def test_create_logging_entry(self):
        """Test creating a PortfolioLog instance."""
        log = PortfolioLog.objects.create(
            symbol="ETH",
            message="Portfolio calculation completed",
            level="INFO"
        )
        assert log.symbol == "ETH"
        assert log.message == "Portfolio calculation completed"
        assert log.level == "INFO"
        assert log.generation_date is not None
