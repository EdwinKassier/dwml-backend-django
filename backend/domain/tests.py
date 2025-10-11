"""Tests for domain app."""

from decimal import Decimal

from django.test import TestCase

from .models import (
    AnalysisReport,
    MarketPrice,
    OpeningAverage,
    PortfolioLog,
    PortfolioResult,
    Prediction,
)
from .services import MarketDataService, PortfolioCalculator, PortfolioService


class PortfolioCalculatorTests(TestCase):
    """Test portfolio calculation logic."""

    def setUp(self):
        self.calculator = PortfolioCalculator()

    def test_calculate_profitable_portfolio(self):
        """Test calculation with profit."""
        result = self.calculator.calculate(
            investment=Decimal("1000"),
            opening_price=Decimal("50000"),
            current_price=Decimal("60000"),
        )

        self.assertEqual(result["number_coins"], Decimal("0.02"))
        self.assertEqual(result["profit"], Decimal("200"))
        self.assertEqual(result["growth_factor"], Decimal("0.2"))

    def test_calculate_loss_portfolio(self):
        """Test calculation with loss."""
        result = self.calculator.calculate(
            investment=Decimal("1000"),
            opening_price=Decimal("60000"),
            current_price=Decimal("50000"),
        )

        self.assertLess(result["profit"], 0)
        self.assertEqual(result["lambos"], Decimal("0"))

    def test_validate_investment_too_low(self):
        """Test validation rejects too low investment."""
        from shared.exceptions.custom_exceptions import ValidationError

        with self.assertRaises(ValidationError):
            self.calculator.validate_investment(Decimal("0.001"))

    def test_validate_investment_too_high(self):
        """Test validation rejects too high investment."""
        from shared.exceptions.custom_exceptions import ValidationError

        with self.assertRaises(ValidationError):
            self.calculator.validate_investment(Decimal("2000000"))


class PortfolioResultModelTests(TestCase):
    """Test PortfolioResult model."""

    def test_create_result(self):
        """Test creating a portfolio result."""
        result = PortfolioResult.objects.create(
            symbol="BTC",
            investment=Decimal("1000"),
            number_coins=Decimal("0.02"),
            profit=Decimal("200"),
            growth_factor=Decimal("0.2"),
            lambos=Decimal("0.001"),
        )

        self.assertEqual(result.symbol, "BTC")
        self.assertEqual(result.roi_percentage, Decimal("20"))
        self.assertTrue(result.is_profitable())
        self.assertFalse(result.can_buy_lambo())
        self.assertEqual(result.risk_level(), "LOW")

    def test_high_risk_portfolio(self):
        """Test high risk level detection."""
        result = PortfolioResult.objects.create(
            symbol="DOGE",
            investment=Decimal("100"),
            number_coins=Decimal("1000"),
            profit=Decimal("500"),
            growth_factor=Decimal("5.0"),
            lambos=Decimal("0.0025"),
        )

        self.assertEqual(result.risk_level(), "HIGH")

    def test_can_buy_lambo(self):
        """Test lamborghini affordability."""
        result = PortfolioResult.objects.create(
            symbol="BTC",
            investment=Decimal("10000"),
            number_coins=Decimal("5"),
            profit=Decimal("300000"),
            growth_factor=Decimal("30"),
            lambos=Decimal("1.5"),
        )

        self.assertTrue(result.can_buy_lambo())


class PortfolioLogModelTests(TestCase):
    """Test PortfolioLog model."""

    def test_create_log(self):
        """Test creating an audit log."""
        log = PortfolioLog.objects.create(
            symbol="ETH",
            action="calculate_portfolio",
            level="INFO",
            metadata={"investment": "1000"},
        )

        self.assertEqual(log.symbol, "ETH")
        self.assertEqual(log.level, "INFO")
        self.assertIn("investment", log.metadata)


class MarketDataModelTests(TestCase):
    """Test market data models."""

    def test_create_opening_average(self):
        """Test creating opening average."""
        avg = OpeningAverage.objects.create(
            symbol="BTC", average=Decimal("50000.12345678")
        )

        self.assertEqual(avg.symbol, "BTC")
        self.assertEqual(avg.average, Decimal("50000.12345678"))

    def test_create_market_price(self):
        """Test creating market price."""
        price = MarketPrice.objects.create(
            symbol="ETH", price=Decimal("3000.5"), volume=Decimal("1000.0")
        )

        self.assertEqual(price.symbol, "ETH")
        self.assertEqual(price.price, Decimal("3000.5"))


class AnalyticsModelTests(TestCase):
    """Test analytics models."""

    def test_create_prediction(self):
        """Test creating a prediction."""
        pred = Prediction.objects.create(
            symbol="BTC",
            prediction_type="covid_impact",
            prediction_data={"severity": "HIGH"},
            confidence=Decimal("85.5"),
        )

        self.assertEqual(pred.prediction_type, "covid_impact")
        self.assertEqual(pred.confidence, Decimal("85.5"))

    def test_create_analysis_report(self):
        """Test creating an analysis report."""
        report = AnalysisReport.objects.create(
            report_type="market_analysis",
            data={"trend": "bullish"},
            summary="Market is trending upward",
        )

        self.assertEqual(report.report_type, "market_analysis")
        self.assertIn("trend", report.data)
