"""Unit tests for Django models."""
import pytest
from django.test import TestCase
from api.models import Results, OPENING_AVERAGE, LOGGING


@pytest.mark.django_db
@pytest.mark.unit
class TestResultsModel:
    """Test cases for Results model."""

    def test_create_result(self):
        """Test creating a Results instance."""
        result = Results.objects.create(
            QUERY="BTC",
            NUMBERCOINS=1.5,
            PROFIT=50000.0,
            GROWTHFACTOR=2.5,
            LAMBOS=0.25,
            INVESTMENT=10000.0,
            SYMBOL="BTC"
        )
        assert result.SYMBOL == "BTC"
        assert result.NUMBERCOINS == 1.5
        assert result.PROFIT == 50000.0
        assert result.id is not None

    def test_result_string_fields(self):
        """Test string field constraints."""
        result = Results.objects.create(
            QUERY="ETH",
            NUMBERCOINS=10.0,
            PROFIT=5000.0,
            GROWTHFACTOR=1.5,
            LAMBOS=0.025,
            INVESTMENT=1000.0,
            SYMBOL="ETH"
        )
        assert len(result.SYMBOL) <= 100
        assert len(result.QUERY) <= 100


@pytest.mark.django_db
@pytest.mark.unit
class TestOpeningAverageModel:
    """Test cases for OPENING_AVERAGE model."""

    def test_create_opening_average(self):
        """Test creating an OPENING_AVERAGE instance."""
        avg = OPENING_AVERAGE.objects.create(
            SYMBOL="BTC",
            AVERAGE=45000.0
        )
        assert avg.SYMBOL == "BTC"
        assert avg.AVERAGE == 45000.0
        assert avg.GENERATIONDATE is not None


@pytest.mark.django_db
@pytest.mark.unit
class TestLoggingModel:
    """Test cases for LOGGING model."""

    def test_create_logging_entry(self):
        """Test creating a LOGGING instance."""
        log = LOGGING.objects.create(
            SYMBOL="ETH",
            INVESTMENT=1000.0
        )
        assert log.SYMBOL == "ETH"
        assert log.INVESTMENT == 1000.0
        assert log.GENERATIONDATE is not None
