"""
Custom exceptions for the Prompt Firewall SDK.
"""


class PromptFirewallError(Exception):
    """Base exception for all SDK errors."""


class APIError(PromptFirewallError):
    """Exception raised for API errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class AuthenticationError(PromptFirewallError):
    """Exception raised for authentication errors."""
