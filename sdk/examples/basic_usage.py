"""
Basic usage example for Prompt Firewall SDK.
"""

from prompt_firewall_sdk import PromptFirewallClient

def main():
    # Initialize client
    client = PromptFirewallClient(base_url="http://localhost:8000")
    
    # Example 1: Process a clean prompt
    print("Example 1: Clean prompt")
    result = client.query(prompt="What is the capital of France?")
    print(f"Decision: {result['decision']}")
    print(f"Explanation: {result['explanation']}")
    print()
    
    # Example 2: Process a prompt with PII
    print("Example 2: Prompt with PII")
    result = client.query(prompt="My email is user@example.com and my SSN is 123-45-6789")
    print(f"Decision: {result['decision']}")
    print(f"Risks detected: {len(result['risks'])}")
    for risk in result['risks']:
        print(f"  - {risk['type']}: {risk['match']} ({risk['severity']})")
    print()
    
    # Example 3: Process a response
    print("Example 3: Process response")
    result = client.query(response="The capital of France is Paris.")
    print(f"Decision: {result['decision']}")
    print()
    
    # Example 4: Health check
    print("Example 4: Health check")
    health = client.health_check()
    print(f"Status: {health['status']}")
    print()
    
    # Close client
    client.close()

if __name__ == "__main__":
    main()

