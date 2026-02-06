import requests
import json
import os

API_KEY = "wjxnmGNampanOgoJAKM7p6crnOfMlmmu2pmFFXqK"
HEADERS = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}' # Trying both styles
}

def test_endpoint(url, method='GET', payload=None):
    print(f"\nTesting {url} [{method}]...")
    try:
        if method == 'GET':
            response = requests.get(url, headers=HEADERS, timeout=10)
        else:
            response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# 1. Test documented Compression Endpoint (to verify key)
payload = {
    "context": "This is a test context.",
    "prompt": "Summarize this.",
    "scaledown": { "rate": "auto" }
}
test_endpoint("https://api.scaledown.xyz/compress/raw/", "POST", payload)

# 2. Test standard OpenAI-compatible Chat Endpoint (hoping it exists)
chat_payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello"}]
}
test_endpoint("https://api.scaledown.xyz/v1/chat/completions", "POST", chat_payload)

# 3. Test Models endpoint
test_endpoint("https://api.scaledown.xyz/v1/models", "GET")
