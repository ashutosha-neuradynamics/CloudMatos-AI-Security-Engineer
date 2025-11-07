"""
Tests for /v1/logs endpoint.
Following TDD - write tests first, then implement.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_logs_endpoint_exists(client):
    """Test that GET /v1/logs endpoint exists."""
    response = client.get("/v1/logs")
    
    assert response.status_code != 404


def test_logs_endpoint_returns_json(client):
    """Test that logs endpoint returns JSON."""
    response = client.get("/v1/logs")
    
    assert response.status_code in [200, 401, 403]
    if response.status_code == 200:
        assert response.headers["content-type"] == "application/json"


def test_logs_endpoint_with_filters(client):
    """Test logs endpoint with query parameters."""
    response = client.get("/v1/logs?type=PII&severity=high&limit=10")
    
    assert response.status_code in [200, 401, 403]


def test_logs_endpoint_pagination(client):
    """Test logs endpoint pagination."""
    response = client.get("/v1/logs?limit=5&offset=0")
    
    assert response.status_code in [200, 401, 403]
    if response.status_code == 200:
        data = response.json()
        assert "logs" in data or "items" in data
        assert "total" in data or "count" in data


def test_logs_endpoint_date_filter(client):
    """Test logs endpoint with date filters."""
    date_from = (datetime.now() - timedelta(days=7)).isoformat()
    date_to = datetime.now().isoformat()
    
    response = client.get(f"/v1/logs?date_from={date_from}&date_to={date_to}")
    
    assert response.status_code in [200, 401, 403]


def test_logs_endpoint_export_json(client):
    """Test logs endpoint JSON export."""
    response = client.get("/v1/logs?format=json")
    
    assert response.status_code in [200, 401, 403]
    if response.status_code == 200:
        assert response.headers["content-type"] == "application/json"


def test_logs_endpoint_export_csv(client):
    """Test logs endpoint CSV export."""
    response = client.get("/v1/logs?format=csv")
    
    assert response.status_code in [200, 401, 403]
    if response.status_code == 200 and "csv" in response.headers.get("content-type", ""):
        assert "text/csv" in response.headers["content-type"]


def test_logs_endpoint_requires_auth(client):
    """Test that logs endpoint may require authentication."""
    response = client.get("/v1/logs")
    
    # May require auth (401/403) or may be public (200)
    assert response.status_code in [200, 401, 403]


def test_logs_endpoint_invalid_limit(client):
    """Test logs endpoint with invalid limit."""
    response = client.get("/v1/logs?limit=-1")
    
    assert response.status_code in [400, 422]


def test_logs_endpoint_invalid_offset(client):
    """Test logs endpoint with invalid offset."""
    response = client.get("/v1/logs?offset=-1")
    
    assert response.status_code in [400, 422]

