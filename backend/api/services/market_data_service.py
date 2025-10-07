"""Market data service for cryptocurrency market information."""

from typing import Dict, Any
from .base_service import BaseService
from ..utils.data_collector import DataCollector
from ..utils.data_cache import DataCache


class MarketDataService(BaseService):
    """Service for market data-related business logic."""
    
    def __init__(self):
        super().__init__()
        self.data_collector = DataCollector()
        self.data_cache = DataCache()
    
    def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current price for a cryptocurrency symbol.
        
        Args:
            symbol: Cryptocurrency symbol
            
        Returns:
            Dict containing current price or error
        """
        try:
            # Check cache first
            cached_price = self.data_cache.get_cached_price(symbol)
            if cached_price:
                return self.success_response({
                    'symbol': symbol,
                    'price': cached_price,
                    'source': 'cache'
                })
            
            # Fetch from external API
            market_data = self.data_collector.get_crypto_data(symbol)
            if not market_data:
                return self.handle_error(
                    Exception(f"No market data found for {symbol}"),
                    "get_current_price"
                )
            
            current_price = market_data.get('current_price', 0)
            
            # Cache the result
            self.data_cache.cache_price(symbol, current_price)
            
            return self.success_response({
                'symbol': symbol,
                'price': current_price,
                'source': 'api'
            })
            
        except Exception as e:
            return self.handle_error(e, "get_current_price")
    
    def get_market_summary(self, symbols: list) -> Dict[str, Any]:
        """
        Get market summary for multiple symbols.
        
        Args:
            symbols: List of cryptocurrency symbols
            
        Returns:
            Dict containing market summary or error
        """
        try:
            summary = {}
            for symbol in symbols:
                price_data = self.get_current_price(symbol)
                if price_data['success']:
                    summary[symbol] = price_data['data']
                else:
                    summary[symbol] = {'error': price_data['error']}
            
            return self.success_response({
                'summary': summary,
                'total_symbols': len(symbols)
            })
            
        except Exception as e:
            return self.handle_error(e, "get_market_summary")
