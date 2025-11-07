"""
Prompt Firewall API client.
"""

from typing import Optional, Dict, List, Any
import httpx
from .exceptions import APIError, AuthenticationError


class PromptFirewallClient:
    """Client for interacting with the Prompt Firewall API."""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the Prompt Firewall client.

        Args:
            base_url: Base URL of the Prompt Firewall API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        self.client = httpx.Client(
            base_url=self.base_url, timeout=30.0, headers=headers
        )

    def query(
        self, prompt: Optional[str] = None, response: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a prompt and/or response through the firewall.

        Args:
            prompt: User's input prompt (optional)
            response: Model's response (optional)

        Returns:
            Dictionary containing firewall decision, modified text, risks, and metadata

        Raises:
            APIError: If the API request fails
        """
        if not prompt and not response:
            raise ValueError("At least one of 'prompt' or 'response' must be provided")

        payload = {}
        if prompt:
            payload["prompt"] = prompt
        if response:
            payload["response"] = response

        try:
            resp = self.client.post("/v1/query", json=payload)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise APIError(
                f"API request failed: {e.response.text}",
                status_code=e.response.status_code,
                response=(
                    e.response.json()
                    if e.response.headers.get("content-type") == "application/json"
                    else None
                ),
            )
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {str(e)}")

    def get_policy(self) -> Dict[str, Any]:
        """
        Retrieve all policy rules.

        Returns:
            Dictionary containing list of policy rules

        Raises:
            APIError: If the API request fails
        """
        try:
            resp = self.client.get("/v1/policy")
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Authentication required")
            raise APIError(
                f"API request failed: {e.response.text}",
                status_code=e.response.status_code,
                response=(
                    e.response.json()
                    if e.response.headers.get("content-type") == "application/json"
                    else None
                ),
            )
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {str(e)}")

    def update_policy(self, rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update policy rules (admin only).

        Args:
            rules: List of policy rule dictionaries

        Returns:
            Dictionary containing updated policy rules

        Raises:
            APIError: If the API request fails
            AuthenticationError: If authentication fails
        """
        payload = {"rules": rules}

        try:
            resp = self.client.put("/v1/policy", json=payload)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Authentication required")
            raise APIError(
                f"API request failed: {e.response.text}",
                status_code=e.response.status_code,
                response=(
                    e.response.json()
                    if e.response.headers.get("content-type") == "application/json"
                    else None
                ),
            )
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {str(e)}")

    def get_logs(
        self,
        type: Optional[str] = None,
        severity: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        format: str = "json",
    ) -> Dict[str, Any]:
        """
        Retrieve firewall logs with filtering and pagination.

        Args:
            type: Filter by risk type (PII, PHI, PROMPT_INJECTION)
            severity: Filter by severity (high, medium, low)
            date_from: Start date (ISO format)
            date_to: End date (ISO format)
            limit: Number of logs to return (1-1000)
            offset: Pagination offset
            format: Export format (json or csv)

        Returns:
            Dictionary containing logs and pagination info (or CSV string if format='csv')

        Raises:
            APIError: If the API request fails
        """
        params = {"limit": limit, "offset": offset, "format": format}
        if type:
            params["type"] = type
        if severity:
            params["severity"] = severity
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to

        try:
            resp = self.client.get("/v1/logs", params=params)
            resp.raise_for_status()
            if format == "csv":
                return resp.text
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Authentication required")
            raise APIError(
                f"API request failed: {e.response.text}",
                status_code=e.response.status_code,
                response=(
                    e.response.json()
                    if e.response.headers.get("content-type") == "application/json"
                    else None
                ),
            )
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {str(e)}")

    def health_check(self) -> Dict[str, Any]:
        """
        Check API health status.

        Returns:
            Dictionary with health status

        Raises:
            APIError: If the API request fails
        """
        try:
            resp = self.client.get("/v1/health")
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {str(e)}")

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
