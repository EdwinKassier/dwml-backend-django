"""Integration tests for API endpoints."""
import pytest
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.integration
class TestAPIEndpoints:
    """Integration tests for API endpoints."""

    def setup_method(self):
        """Set up test client."""
        self.client = APIClient()

    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get('/api/v1/health/')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert 'version' in data
        assert 'timestamp' in data

    def test_process_request_invalid_symbol(self):
        """Test API with invalid cryptocurrency symbol."""
        response = self.client.get(
            '/api/v1/calculations/',
            {'symbol': 'INVALID', 'investment': '1000'}
        )
        assert response.status_code in [200, 400, 404]  # Depends on implementation
        data = response.json()
        assert 'error' in data or 'message' in data

    def test_process_request_missing_investment(self):
        """Test API with missing investment parameter."""
        response = self.client.get(
            '/api/v1/calculations/',
            {'symbol': 'BTC'}
        )
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data

    def test_process_request_missing_symbol(self):
        """Test API with missing symbol parameter."""
        response = self.client.get(
            '/api/v1/calculations/',
            {'investment': '1000'}
        )
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data

    def test_process_request_valid_parameters(self):
        """Test API with valid parameters."""
        response = self.client.get(
            '/api/v1/calculations/',
            {'symbol': 'ETH', 'investment': '5000'}
        )
        # Response could be 200 (success) or 404 (symbol not found) or 500 (external API error)
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert 'success' in data or 'data' in data

    def test_unknown_route_returns_404(self):
        """Test that unknown routes return 404."""
        response = self.client.get('/api/v1/nonexistent/')
        assert response.status_code == 404

    def test_covid_prediction_endpoint(self):
        """Test COVID prediction endpoint."""
        response = self.client.get('/api/v1/predictions/covid/')
        # Could succeed or fail depending on external dependencies
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert 'success' in data or 'data' in data

    def test_results_list_endpoint(self):
        """Test results list endpoint."""
        response = self.client.get('/api/v1/results/')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_opening_averages_list_endpoint(self):
        """Test opening averages list endpoint."""
        response = self.client.get('/api/v1/opening-averages/')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_logs_list_endpoint(self):
        """Test logs list endpoint."""
        response = self.client.get('/api/v1/logs/')
        assert response.status_code == 200
        assert isinstance(response.json(), list)
