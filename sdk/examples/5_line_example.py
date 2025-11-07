"""
5-line integration example for Prompt Firewall SDK.
"""

from prompt_firewall_sdk import PromptFirewallClient
client = PromptFirewallClient(base_url="http://localhost:8000")
result = client.query(prompt="My email is user@example.com")
if result['decision'] == 'block':
    raise ValueError("Request blocked by firewall")
print(result['explanation'])

