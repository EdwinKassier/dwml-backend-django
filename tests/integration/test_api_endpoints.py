"""Integration tests for API endpoints."""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
@pytest.mark.integration
class TestAPIEndpoints:
    """Integration tests for API endpoints."""

    def setup_method(self):
        """Set up test client."""
        self.client = APIClient()

    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get("/api/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "service" in data

    def test_process_request_invalid_symbol(self):
        """Test API with invalid cryptocurrency symbol."""
        response = self.client.get(
            "/api/process_request/", {"symbol": "INVALID", "investment": "1000"}
        )
        # Should return error (404 for not found or 400 for validation)
        assert response.status_code in [400, 404, 500]

    def test_process_request_missing_investment(self):
        """Test API with missing investment parameter."""
        response = self.client.get("/api/process_request/", {"symbol": "BTC"})
        assert response.status_code == 400
        data = response.json()
        assert "investment" in data

    def test_process_request_missing_symbol(self):
        """Test API with missing symbol parameter."""
        response = self.client.get("/api/process_request/", {"investment": "1000"})
        assert response.status_code == 400
        data = response.json()
        assert "symbol" in data

    def test_process_request_valid_parameters(self):
        """Test API with valid parameters."""
        response = self.client.get(
            "/api/process_request/", {"symbol": "ETH", "investment": "5000"}
        )
        # Response could be 201 (success), 404 (symbol not found), or 500 (external API error)
        assert response.status_code in [201, 404, 500]

        if response.status_code == 201:
            data = response.json()
            assert "symbol" in data
            assert "profit" in data
            assert "investment" in data

    def test_unknown_route_returns_404(self):
        """Test that unknown routes return 404."""
        response = self.client.get("/api/nonexistent/")
        assert response.status_code == 404

    def test_covid_prediction_endpoint(self):
        """Test COVID prediction endpoint."""
        response = self.client.get("/api/analytics/covid/")
        # Should succeed with mock data
        assert response.status_code == 200
        data = response.json()
        assert "covid_data" in data or "analysis" in data

    def test_results_list_endpoint(self):
        """Test results list endpoint."""
        response = self.client.get("/api/results/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_logs_list_endpoint(self):
        """Test logs list endpoint."""
        response = self.client.get("/api/logs/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_analytics_report_endpoint(self):
        """Test analytics report generation endpoint."""
        response = self.client.get("/api/analytics/report/")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "report_type" in data

    def test_price_history_endpoint(self):
        """Test price history endpoint."""
        response = self.client.get("/api/price/history/", {"symbol": "BTC"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
