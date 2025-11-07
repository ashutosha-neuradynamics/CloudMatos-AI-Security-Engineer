# Prompt Firewall SDK

Python SDK for the Prompt Firewall API - a security firewall for detecting PII/PHI and prompt injections in LLM interactions.

## Installation

```bash
pip install prompt-firewall-sdk
```

Or install from source:

```bash
cd sdk
pip install -e .
```

## Quick Start

```python
from prompt_firewall_sdk import PromptFirewallClient

# Initialize client
client = PromptFirewallClient(base_url="http://localhost:8000")

# Process a prompt
result = client.query(prompt="What is the capital of France?")
print(f"Decision: {result['decision']}")
print(f"Risks: {result['risks']}")
```

## 5-Line Integration Example

```python
from prompt_firewall_sdk import PromptFirewallClient
client = PromptFirewallClient(base_url="http://localhost:8000")
result = client.query(prompt="My email is user@example.com")
if result['decision'] == 'block':
    raise ValueError("Request blocked by firewall")
print(result['explanation'])
```

## Usage

### Initialize Client

```python
from prompt_firewall_sdk import PromptFirewallClient

client = PromptFirewallClient(
    base_url="http://localhost:8000",
    api_key="your-api-key"  # Optional
)
```

### Process Queries

```python
# Process a prompt
result = client.query(prompt="What is the capital of France?")

# Process a response
result = client.query(response="The capital of France is Paris.")

# Process both
result = client.query(
    prompt="What is the capital of France?",
    response="The capital of France is Paris."
)
```

### Get Policy Rules

```python
# Get all policy rules
policy = client.get_policy()
print(policy['rules'])

# Update policy rules (admin only)
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
updated = client.update_policy(rules)
```

### Retrieve Logs

```python
# Get logs with default pagination
logs = client.get_logs()

# Get logs with filters
logs = client.get_logs(
    type="PII",
    severity="high",
    date_from="2024-01-01T00:00:00Z",
    date_to="2024-01-31T23:59:59Z",
    limit=100,
    offset=0
)

# Export logs as CSV
csv_data = client.get_logs(format="csv")
```

### Health Check

```python
health = client.health_check()
print(health['status'])
```

### Context Manager

```python
with PromptFirewallClient(base_url="http://localhost:8000") as client:
    result = client.query(prompt="test")
    # Client automatically closes when exiting context
```

## Error Handling

```python
from prompt_firewall_sdk import PromptFirewallClient, APIError, AuthenticationError

client = PromptFirewallClient(base_url="http://localhost:8000")

try:
    result = client.query(prompt="test")
except AuthenticationError:
    print("Authentication failed")
except APIError as e:
    print(f"API error: {e.message} (Status: {e.status_code})")
```

## API Reference

### PromptFirewallClient

#### Methods

- `query(prompt=None, response=None)` - Process prompt/response through firewall
- `get_policy()` - Retrieve all policy rules
- `update_policy(rules)` - Update policy rules (admin only)
- `get_logs(type=None, severity=None, date_from=None, date_to=None, limit=50, offset=0, format='json')` - Retrieve logs
- `health_check()` - Check API health status
- `close()` - Close the HTTP client

## Development

### Running Tests

```bash
cd sdk
pytest
```

### Building Package

```bash
cd sdk
python -m build
```

## License

MIT

