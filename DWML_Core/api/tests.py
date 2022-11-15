
from rest_framework.test import APIClient
import pytest


client = APIClient()



@pytest.mark.django_db
def test_base_route_with_args_invalid_symbol():
    """Test base route with invalid symbol"""
    response = client.get('/api/v1/process_request/?symbol=DUHHH&investment=1000')

    print(response.json())

    assert response.status_code == 200
    assert response.json() == {
        'message': "Symbol doesn't exist", 'graph_data': "Symbol doesn't exist"}

@pytest.mark.django_db
def test_base_route_malformed_no_symbol():
    """Test base route with missing symbol"""
    response = client.get('/api/v1/process_request/?investment=1000')

    assert response.json() == {
        'message': "Symbol doesn't exist", 'graph_data': "Symbol doesn't exist"}

    assert response.status_code == 200

@pytest.mark.django_db
def test_base_route_malformed_no_investment():
    """Test base route with missing investment"""
    response = client.get('/api/v1/process_request/?symbol=BTC')

    assert response.status_code == 400

@pytest.mark.django_db
def test_unknown_route():
    """Test a route that isn't supported"""
    response = client.get('/random')

    assert response.status_code == 404


'''
@pytest.mark.django_db
def test_base_route_without_args():
    """Test base route with no arguments given"""
    response = client.get('/process_request')

    assert response.status_code == 422

@pytest.mark.django_db
def test_base_route_with_args_invalid_symbol():
    """Test base route with invalid symbol"""
    response = client.get('/process_request?symbol=DUHHH&investment=1000')

    print(response.json())

    assert response.status_code == 200
    assert response.json() == {
        'message': "Symbol doesn't exist", 'graph_data': "Symbol doesn't exist"}

@pytest.mark.django_db
def test_base_route_malformed_no_symbol():
    """Test base route with missing symbol"""
    response = client.get('/process_request?investment=1000')

    print(response.json())

    assert response.status_code == 422

@pytest.mark.django_db
def test_base_route_malformed_no_investment():
    """Test base route with missing investment"""
    response = client.get('/process_request?symbol=BTC')

    assert response.status_code == 422

@pytest.mark.django_db
def test_unknown_route():
    """Test a route that isn't supported"""
    response = client.get('/random')

    assert response.status_code == 404
'''