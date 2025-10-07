"""Custom exceptions for the application."""


class CryptoAPIException(Exception):
    """Base exception for Crypto API."""
    pass


class MarketDataException(CryptoAPIException):
    """Exception for market data related errors."""
    pass


class PortfolioException(CryptoAPIException):
    """Exception for portfolio related errors."""
    pass


class AnalyticsException(CryptoAPIException):
    """Exception for analytics related errors."""
    pass


class ExternalAPIException(CryptoAPIException):
    """Exception for external API errors."""
    pass
