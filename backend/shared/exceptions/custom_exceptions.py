"""
Domain exceptions for clear error handling.
Use exceptions, not dict returns with 'success' keys.
"""


class DomainException(Exception):
    """Base exception for all domain errors."""

    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code or self.__class__.__name__
        super().__init__(self.message)


class ValidationError(DomainException):
    """Input validation failed."""

    pass


class NotFoundError(DomainException):
    """Resource not found."""

    pass


class ExternalServiceError(DomainException):
    """External service unavailable or failed."""

    pass


class BusinessRuleError(DomainException):
    """Business rule violation."""

    pass


# Legacy exception classes for backwards compatibility
class CryptoAPIException(DomainException):
    """Base exception for Crypto API (legacy)."""

    pass


class MarketDataException(CryptoAPIException):
    """Exception for market data related errors (legacy)."""

    pass


class PortfolioException(CryptoAPIException):
    """Exception for portfolio related errors (legacy)."""

    pass


class AnalyticsException(CryptoAPIException):
    """Exception for analytics related errors (legacy)."""

    pass


class ExternalAPIException(ExternalServiceError):
    """Exception for external API errors (legacy)."""

    pass
