"""
Tests for PromptFirewallClient.
"""

import pytest
from unittest.mock import Mock, patch
import httpx
from prompt_firewall_sdk import PromptFirewallClient
from prompt_firewall_sdk.exceptions import APIError, AuthenticationError


class TestClientInitialization:
    """Tests for client initialization."""
    
    def test_init_with_base_url(self):
        """Test client initialization with base URL."""
        client = PromptFirewallClient(base_url="http://localhost:8000")
        assert client.base_url == "http://localhost:8000"
        assert client.api_key is None
        client.close()
    
    def test_init_with_api_key(self):
        """Test client initialization with API key."""
        client = PromptFirewallClient(
            base_url="http://localhost:8000",
            api_key="test-key"
        )
        assert client.base_url == "http://localhost:8000"
        assert client.api_key == "test-key"
        client.close()
    
    def test_init_strips_trailing_slash(self):
        """Test that trailing slash is stripped from base URL."""
        client = PromptFirewallClient(base_url="http://localhost:8000/")
        assert client.base_url == "http://localhost:8000"
        client.close()
    
    def test_context_manager(self):
        """Test client as context manager."""
        with PromptFirewallClient(base_url="http://localhost:8000") as client:
            assert client.base_url == "http://localhost:8000"
        # Client should be closed after context exit


class TestQueryMethod:
    """Tests for query method."""
    
    @patch('httpx.Client')
    def test_query_with_prompt(self, mock_client_class):
        """Test query method with prompt."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "decision": "allow",
            "promptModified": None,
            "responseModified": None,
            "risks": [],
            "explanation": "No risks detected",
            "metadata": {"requestId": "test-id", "timestamp": "2024-01-01T00:00:00Z"}
        }
        mock_response.raise_for_status = Mock()
        
        mock_client = Mock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        client = PromptFirewallClient(base_url="http://localhost:8000")
        result = client.query(prompt="What is the capital of France?")
        
        assert result["decision"] == "allow"
        mock_client.post.assert_called_once_with(
            "/v1/query",
            json={"prompt": "What is the capital of France?"}
        )
        client.close()
    
    @patch('httpx.Client')
    def test_query_with_response(self, mock_client_class):
        """Test query method with response."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "decision": "allow",
            "promptModified": None,
            "responseModified": None,
            "risks": [],
            "explanation": "No risks detected",
            "metadata": {"requestId": "test-id", "timestamp": "2024-01-01T00:00:00Z"}
        }
        mock_response.raise_for_status = Mock()
        
        mock_client = Mock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        client = PromptFirewallClient(base_url="http://localhost:8000")
        result = client.query(response="The capital of France is Paris.")
        
        assert result["decision"] == "allow"
        mock_client.post.assert_called_once_with(
            "/v1/query",
            json={"response": "The capital of France is Paris."}
        )
        client.close()
    
    @patch('httpx.Client')
    def test_query_with_both(self, mock_client_class):
        """Test query method with both prompt and response."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "decision": "allow",
            "promptModified": None,
            "responseModified": None,
            "risks": [],
            "explanation": "No risks detected",
            "metadata": {"requestId": "test-id", "timestamp": "2024-01-01T00:00:00Z"}
        }
        mock_response.raise_for_status = Mock()
        
        mock_client = Mock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        client = PromptFirewallClient(base_url="http://localhost:8000")
        result = client.query(
            prompt="What is the capital of France?",
            response="The capital of France is Paris."
        )
        
        assert result["decision"] == "allow"
        mock_client.post.assert_called_once_with(
            "/v1/query",
            json={
                "prompt": "What is the capital of France?",
                "response": "The capital of France is Paris."
            }
        )
        client.close()
    
    def test_query_without_prompt_or_response(self):
        """Test query method raises error when neither prompt nor response provided."""
        client = PromptFirewallClient(base_url="http://localhost:8000")
        with pytest.raises(ValueError, match="At least one of 'prompt' or 'response' must be provided"):
            client.query()
        client.close()
    
    @patch('httpx.Client')
    def test_query_api_error(self, mock_client_class):
        """Test query method handles API errors."""
        mock_response = Mock()
        mock_response.text = "Internal Server Error"
        mock_response.status_code = 500
        mock_response.headers = {"content-type": "application/json"}
        mock_response.json.return_value = {"detail": "Internal Server Error"}
        
        mock_client = Mock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        error = httpx.HTTPStatusError("Server Error", request=Mock(), response=mock_response)
        mock_client.post.side_effect = error
        
        client = PromptFirewallClient(base_url="http://localhost:8000")
        with pytest.raises(APIError) as exc_info:
            client.query(prompt="test")
        
        assert exc_info.value.status_code == 500
        client.close()


class TestPolicyMethods:
    """Tests for policy methods."""
    
    @patch('httpx.Client')
    def test_get_policy(self, mock_client_class):
        """Test get_policy method."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "rules": [
                {
                    "id": 1,
                    "name": "Block PII",
                    "risk_type": "PII",
                    "pattern": ".*",
                    "severity": "high",
                    "action": "block",
                    "enabled": True
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        client = PromptFirewallClient(base_url="http://localhost:8000")
        result = client.get_policy()
        
        assert "rules" in result
        assert len(result["rules"]) == 1
        mock_client.get.assert_called_once_with("/v1/policy")
        client.close()
    
    @patch('httpx.Client')
    def test_update_policy(self, mock_client_class):
        """Test update_policy method."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "rules": [
                {
                    "id": 1,
                    "name": "Block PII",
                    "risk_type": "PII",
                    "pattern": ".*",
                    "severity": "high",
                    "action": "block",
                    "enabled": True
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        
        mock_client = Mock()
        mock_client.put.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        client = PromptFirewallClient(base_url="http://localhost:8000")
        rules = [
            {
                "name": "Block PII",
                "risk_type": "PII",
                "pattern": ".*",
                "pattern_type": "regex",
                "severity": "high",
                "action": "block",
                "enabled": True
            }
        ]
        result = client.update_policy(rules)
        
        assert "rules" in result
        mock_client.put.assert_called_once_with("/v1/policy", json={"rules": rules})
        client.close()
    
    @patch('httpx.Client')
    def test_get_policy_authentication_error(self, mock_client_class):
        """Test get_policy raises AuthenticationError on 401."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_response.headers = {}
        
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        error = httpx.HTTPStatusError("Unauthorized", request=Mock(), response=mock_response)
        mock_client.get.side_effect = error
        
        client = PromptFirewallClient(base_url="http://localhost:8000")
        with pytest.raises(AuthenticationError):
            client.get_policy()
        client.close()


class TestLogsMethod:
    """Tests for logs method."""
    
    @patch('httpx.Client')
    def test_get_logs_default(self, mock_client_class):
        """Test get_logs with default parameters."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "logs": [],
            "total": 0,
            "limit": 50,
            "offset": 0,
            "has_more": False
        }
        mock_response.raise_for_status = Mock()
        
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        client = PromptFirewallClient(base_url="http://localhost:8000")
        result = client.get_logs()
        
        assert "logs" in result
        mock_client.get.assert_called_once_with(
            "/v1/logs",
            params={"limit": 50, "offset": 0, "format": "json"}
        )
        client.close()
    
    @patch('httpx.Client')
    def test_get_logs_with_filters(self, mock_client_class):
        """Test get_logs with filters."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "logs": [],
            "total": 0,
            "limit": 10,
            "offset": 0,
            "has_more": False
        }
        mock_response.raise_for_status = Mock()
        
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        client = PromptFirewallClient(base_url="http://localhost:8000")
        result = client.get_logs(
            type="PII",
            severity="high",
            date_from="2024-01-01T00:00:00Z",
            date_to="2024-01-31T23:59:59Z",
            limit=10,
            offset=0
        )
        
        assert "logs" in result
        mock_client.get.assert_called_once_with(
            "/v1/logs",
            params={
                "type": "PII",
                "severity": "high",
                "date_from": "2024-01-01T00:00:00Z",
                "date_to": "2024-01-31T23:59:59Z",
                "limit": 10,
                "offset": 0,
                "format": "json"
            }
        )
        client.close()
    
    @patch('httpx.Client')
    def test_get_logs_csv_format(self, mock_client_class):
        """Test get_logs with CSV format."""
        mock_response = Mock()
        mock_response.text = "id,request_id,timestamp,decision\n1,test-id,2024-01-01,allow"
        mock_response.raise_for_status = Mock()
        
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        client = PromptFirewallClient(base_url="http://localhost:8000")
        result = client.get_logs(format="csv")
        
        assert isinstance(result, str)
        assert "id,request_id" in result
        mock_client.get.assert_called_once_with(
            "/v1/logs",
            params={"limit": 50, "offset": 0, "format": "csv"}
        )
        client.close()


class TestHealthCheck:
    """Tests for health check method."""
    
    @patch('httpx.Client')
    def test_health_check(self, mock_client_class):
        """Test health_check method."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "healthy"}
        mock_response.raise_for_status = Mock()
        
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        client = PromptFirewallClient(base_url="http://localhost:8000")
        result = client.health_check()
        
        assert result["status"] == "healthy"
        mock_client.get.assert_called_once_with("/v1/health")
        client.close()

