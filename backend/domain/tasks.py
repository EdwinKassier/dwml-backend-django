"""
Celery tasks for the domain app.

DESIGN PATTERN:
Tasks are thin wrappers around domain services. Business logic
should live in services.py, not in tasks. This ensures:
- Service logic is testable independently
- Service can be called synchronously or asynchronously
- Single source of truth for business logic

EXAMPLE USAGE:
    # Good: Task calls service
    @shared_task(name='domain.process_data')
    def process_data_task(data_id):
        service = MyService()
        return service.process(data_id)

    # Bad: Task contains business logic
    @shared_task(name='domain.process_data')
    def process_data_task(data_id):
        # Business logic here (duplicates service)
        pass

Replace these example tasks with your own domain-specific tasks.
"""
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from celery import shared_task
from celery.utils.log import get_task_logger
from shared.exceptions.custom_exceptions import ExternalServiceError, ValidationError

logger = get_task_logger(__name__)


# =============================================================================
# PORTFOLIO TASKS (Example - integrates with PortfolioService)
# =============================================================================


@shared_task(name="domain.process_portfolio_async", bind=True, max_retries=3)
def process_portfolio_async(self, symbol: str, investment: float):
    """
    Process portfolio calculation asynchronously.

    This task wraps PortfolioService.process_request() for async execution.
    Business logic stays in the service layer.

    Usage:
        # From a view or another task
        result = process_portfolio_async.delay(symbol="BTC", investment=1000.0)
        task_id = result.task_id

    Args:
        self: Task instance (when bind=True)
        symbol: Cryptocurrency symbol (e.g., 'BTC')
        investment: Investment amount in USD

    Returns:
        dict: Result with portfolio ID and key metrics

    Raises:
        ValidationError: If inputs are invalid (not retried)
        ExternalServiceError: If external API fails (retried)
    """
    from .services import PortfolioService

    logger.info(f"Processing portfolio async: {symbol}, ${investment}")

    try:
        service = PortfolioService()
        result = service.process_request(
            symbol=symbol, investment=Decimal(str(investment))
        )

        logger.info(f"Portfolio processed successfully: ID {result.id}")

        return {
            "result_id": result.id,
            "symbol": result.symbol,
            "investment": float(result.investment),
            "profit": float(result.profit),
            "roi_percentage": float(result.roi_percentage),
            "is_profitable": result.is_profitable(),
        }

    except ValidationError as e:
        # Domain validation error - don't retry
        logger.error(f"Validation error in portfolio processing: {e}")
        raise

    except ExternalServiceError as e:
        # External service error - retry with backoff
        logger.warning(f"External service error, will retry: {e}")
        raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))


# =============================================================================
# MARKET DATA TASKS (Example - integrates with MarketDataService)
# =============================================================================


@shared_task(name="domain.fetch_market_prices")
def fetch_market_prices_task():
    """
    Fetch and cache current market prices for all tracked symbols.

    This task should be scheduled to run periodically (e.g., every 5 minutes)
    using Celery Beat.

    Schedule in Django admin:
        - Periodic Task: "Fetch Market Prices"
        - Task: domain.fetch_market_prices
        - Interval: Every 5 minutes
        - Enabled: ✓

    Returns:
        dict: Symbol -> price mapping with fetch status
    """
    from .services import MarketDataService

    # Define symbols to track (replace with your own)
    symbols = ["BTC", "ETH", "ADA", "SOL", "XRP"]

    logger.info(f"Fetching market prices for {len(symbols)} symbols")

    service = MarketDataService()
    results = {}

    for symbol in symbols:
        try:
            price = service.get_current_price(symbol)
            results[symbol] = {
                "price": float(price),
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
            }
            logger.info(f"Fetched {symbol}: ${price}")

        except Exception as e:  # noqa: BLE001 - Catch all to continue processing
            results[symbol] = {"price": None, "status": "error", "error": str(e)}
            logger.error(f"Failed to fetch {symbol}: {e}")

    success_count = sum(1 for r in results.values() if r["status"] == "success")
    logger.info(
        f"Market price fetch completed: {success_count}/{len(symbols)} successful"
    )

    return results


@shared_task(name="domain.update_opening_averages")
def update_opening_averages_task():
    """
    Calculate and update opening averages for tracked symbols.

    This task should be scheduled to run daily.

    Schedule in Django admin:
        - Periodic Task: "Update Opening Averages"
        - Task: domain.update_opening_averages
        - Interval: Every 1 day
        - Enabled: ✓

    Returns:
        dict: Update results for each symbol
    """
    from .services import MarketDataService

    symbols = ["BTC", "ETH", "ADA", "SOL", "XRP"]

    logger.info(f"Updating opening averages for {len(symbols)} symbols")

    service = MarketDataService()
    results = {}

    for symbol in symbols:
        try:
            average = service.get_opening_average(symbol)
            results[symbol] = {
                "average": float(average),
                "status": "success",
            }
            logger.info(f"Updated {symbol} opening average: ${average}")

        except Exception as e:  # noqa: BLE001 - Catch all to continue processing
            results[symbol] = {"average": None, "status": "error", "error": str(e)}
            logger.error(f"Failed to update {symbol} opening average: {e}")

    return results


# =============================================================================
# ANALYTICS TASKS (Example - integrates with AnalyticsService)
# =============================================================================


@shared_task(name="domain.generate_analytics_report")
def generate_analytics_report_task(symbol: Optional[str] = None):
    """
    Generate comprehensive analytics report.

    Can be triggered manually or scheduled to run daily.

    Usage:
        # Generate report for all symbols
        generate_analytics_report_task.delay()

        # Generate report for specific symbol
        generate_analytics_report_task.delay(symbol="BTC")

    Args:
        symbol: Optional symbol to filter by (None = all symbols)

    Returns:
        dict: Analytics report with key metrics
    """
    from .services import AnalyticsService

    logger.info(f"Generating analytics report for {symbol or 'all symbols'}")

    service = AnalyticsService()
    report = service.generate_report(symbol=symbol)

    logger.info(
        f"Report generated: {report['total_calculations']} calculations analyzed"
    )

    return report


@shared_task(name="domain.analyze_covid_impact")
def analyze_covid_impact_task():
    """
    Analyze COVID-19 impact on cryptocurrency market.

    This task can be scheduled or triggered manually.

    Returns:
        dict: COVID impact analysis
    """
    from .services import AnalyticsService

    logger.info("Analyzing COVID-19 market impact")

    service = AnalyticsService()
    prediction = service.get_covid_prediction()

    logger.info("COVID impact analysis completed")

    return prediction


# =============================================================================
# MAINTENANCE TASKS (Example - direct domain operations)
# =============================================================================


@shared_task(name="domain.cleanup_old_data")
def cleanup_old_data_task(days: int = 90):
    """
    Clean up old portfolio results and market data.

    This task should be scheduled to run daily, typically at off-peak hours.

    Schedule in Django admin:
        - Periodic Task: "Daily Data Cleanup"
        - Task: domain.cleanup_old_data
        - Interval: Every 1 day at 2:00 AM
        - Args: [90]  # Keep last 90 days
        - Enabled: ✓

    Args:
        days: Number of days to keep (default: 90)

    Returns:
        dict: Cleanup statistics
    """
    from .models import MarketPrice, PortfolioLog, PortfolioResult

    threshold = datetime.now() - timedelta(days=days)

    logger.info(f"Cleaning up data older than {threshold.date()}")

    # Delete old portfolio results
    deleted_results = PortfolioResult.objects.filter(
        generation_date__lt=threshold
    ).delete()

    # Delete old market prices
    deleted_prices = MarketPrice.objects.filter(timestamp__lt=threshold).delete()

    # Delete old logs (keep for shorter period - 30 days)
    log_threshold = datetime.now() - timedelta(days=30)
    deleted_logs = PortfolioLog.objects.filter(created_at__lt=log_threshold).delete()

    result = {
        "threshold_date": threshold.isoformat(),
        "days_retained": days,
        "deleted_results": deleted_results[0] if deleted_results else 0,
        "deleted_prices": deleted_prices[0] if deleted_prices else 0,
        "deleted_logs": deleted_logs[0] if deleted_logs else 0,
        "timestamp": datetime.utcnow().isoformat(),
    }

    logger.info(
        f"Cleanup completed: {result['deleted_results']} results, "
        f"{result['deleted_prices']} prices, {result['deleted_logs']} logs deleted"
    )

    return result


@shared_task(name="domain.log_system_event")
def log_system_event_task(action: str, level: str = "INFO", metadata: dict = None):
    """
    Log system events to PortfolioLog.

    Simple task for logging system events without complex business logic.

    Usage:
        log_system_event_task.delay(
            action="System maintenance completed",
            level="INFO",
            metadata={"tasks_run": 5, "duration": "2m"}
        )

    Args:
        action: Description of the event
        level: Log level (INFO, WARN, ERROR)
        metadata: Optional metadata dictionary

    Returns:
        int: ID of created log entry
    """
    from .models import PortfolioLog

    logger.info(f"Logging system event: {action} ({level})")

    log_entry = PortfolioLog.objects.create(
        symbol="SYSTEM",
        action=action,
        level=level,
        metadata=metadata or {},
    )

    return log_entry.id


# =============================================================================
# BATCH PROCESSING TASKS (Example - processing multiple items)
# =============================================================================


@shared_task(name="domain.batch_process_portfolios", bind=True)
def batch_process_portfolios_task(self, portfolio_configs: list):
    """
    Process multiple portfolio calculations in batch.

    Useful for backtesting or bulk processing scenarios.

    Usage:
        configs = [
            {"symbol": "BTC", "investment": 1000},
            {"symbol": "ETH", "investment": 2000},
            {"symbol": "ADA", "investment": 500},
        ]
        task = batch_process_portfolios_task.delay(configs)

    Args:
        self: Task instance
        portfolio_configs: List of {"symbol": str, "investment": float} dicts

    Returns:
        dict: Processing results
    """
    from .services import PortfolioService

    total = len(portfolio_configs)
    logger.info(f"Starting batch processing for {total} portfolios")

    service = PortfolioService()
    processed = 0
    errors = []
    results = []

    for idx, config in enumerate(portfolio_configs):
        try:
            result = service.process_request(
                symbol=config["symbol"], investment=Decimal(str(config["investment"]))
            )

            results.append(
                {
                    "symbol": config["symbol"],
                    "result_id": result.id,
                    "profit": float(result.profit),
                    "status": "success",
                }
            )

            processed += 1

            # Update task progress
            self.update_state(
                state="PROGRESS",
                meta={
                    "current": idx + 1,
                    "total": total,
                    "percent": int((idx + 1) / total * 100),
                    "processed": processed,
                },
            )

        except Exception as e:  # noqa: BLE001 - Catch all to continue batch
            logger.error(f"Failed to process {config['symbol']}: {e}")
            errors.append(
                {
                    "symbol": config["symbol"],
                    "investment": config["investment"],
                    "error": str(e),
                }
            )

    summary = {
        "total": total,
        "processed": processed,
        "errors": len(errors),
        "error_details": errors,
        "results": results,
    }

    logger.info(f"Batch processing completed: {processed}/{total} successful")

    return summary
