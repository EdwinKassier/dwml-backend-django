"""Unit tests for API serializers."""
import pytest
from domain.serializers import CalculationRequestSerializer
from rest_framework import serializers


@pytest.mark.unit
class TestCalculationRequestSerializer:
    """Test cases for CalculationRequestSerializer."""

    def test_valid_data(self):
        """Test serializer with valid data."""
        data = {"symbol": "BTC", "investment": "1000.50"}
        serializer = CalculationRequestSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["symbol"] == "BTC"
        assert float(serializer.validated_data["investment"]) == 1000.50

    def test_symbol_validation(self):
        """Test symbol field validation."""
        # Test invalid characters
        data = {"symbol": "btc-invalid!", "investment": "1000"}
        serializer = CalculationRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "symbol" in serializer.errors

        # Test too short
        data = {"symbol": "B", "investment": "1000"}
        serializer = CalculationRequestSerializer(data=data)
        assert not serializer.is_valid()

        # Test too long
        data = {"symbol": "VERYLONGSYMBOL", "investment": "1000"}
        serializer = CalculationRequestSerializer(data=data)
        assert not serializer.is_valid()

    def test_investment_validation(self):
        """Test investment field validation."""
        # Test negative investment
        data = {"symbol": "BTC", "investment": "-100"}
        serializer = CalculationRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "investment" in serializer.errors

        # Test zero investment
        data = {"symbol": "BTC", "investment": "0"}
        serializer = CalculationRequestSerializer(data=data)
        assert not serializer.is_valid()

        # Test too large investment
        data = {"symbol": "BTC", "investment": "2000000"}
        serializer = CalculationRequestSerializer(data=data)
        assert not serializer.is_valid()

    def test_symbol_case_handling(self):
        """Test that symbol is converted to uppercase."""
        data = {"symbol": "btc", "investment": "1000"}
        serializer = CalculationRequestSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["symbol"] == "BTC"

    def test_missing_fields(self):
        """Test validation with missing fields."""
        # Missing symbol
        data = {"investment": "1000"}
        serializer = CalculationRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "symbol" in serializer.errors

        # Missing investment
        data = {"symbol": "BTC"}
        serializer = CalculationRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "investment" in serializer.errors

        # Missing both
        data = {}
        serializer = CalculationRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "symbol" in serializer.errors
        assert "investment" in serializer.errors
