"""Base service class for common functionality."""

import logging
from typing import Dict, Any


class BaseService:
    """Base service class providing common functionality."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle errors consistently across services."""
        self.logger.exception(f"Error in {context}: {str(error)}")
        return {"success": False, "error": str(error), "context": context}

    def success_response(self, data: Any) -> Dict[str, Any]:
        """Create consistent success response."""
        return {"success": True, "data": data}
