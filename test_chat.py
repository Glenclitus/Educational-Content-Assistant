import urllib.request
import json
import sys

def test_chat():
    url = "http://localhost:5000/api/ask"
    
    # payload with a dummy pdf_id (assuming 1 exists or handling 404/fallback)
    # The server checks DB. We might need to upload a file first or assume one exists.
    # Let's try to upload one first or check modules.
    
    # 1. Check modules
    try:
        with urllib.request.urlopen("http://localhost:5000/api/modules") as response:
            data = json.loads(response.read().decode())
            modules = data.get('modules', [])
            if not modules:
                print("No modules found. Cannot test chat without a module.")
                # Try to create a dummy concept (manual entry)
                print("Creating dummy concept...")
                req = urllib.request.Request(
                    "http://localhost:5000/api/save-concept",
                    data=json.dumps({"module_name": "Test Module", "content": "This is a test content about Python programming."}).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req) as resp:
                    res_data = json.loads(resp.read().decode())
                    pdf_id = res_data['module_id']
                    print(f"Created module with ID: {pdf_id}")
            else:
                pdf_id = modules[0]['id']
                print(f"Using existing module ID: {pdf_id}")
                
                
            # 2. Ask question WITHOUT pdf_id (General Knowledge Test)
            print("\nTesting General Knowledge Chat (No PDF ID)...")
            req = urllib.request.Request(
                url,
                data=json.dumps({"question": "What is the capital of France?"}).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            try:
                with urllib.request.urlopen(req) as response:
                    answer_data = json.loads(response.read().decode())
                    print("Response received:")
                    print(json.dumps(answer_data, indent=2))
            except urllib.error.HTTPError as e:
                print(f"Error asking general question: {e.read().decode()}")

            # 3. Ask question with pdf_id
            print(f"\nAsking question for module {pdf_id}...")
            req = urllib.request.Request(
                url,
                data=json.dumps({"pdf_id": pdf_id, "question": "What is this content about?"}).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            try:
                with urllib.request.urlopen(req) as response:
                    answer_data = json.loads(response.read().decode())
                    print("Response received:")
                    print(json.dumps(answer_data, indent=2))
            except urllib.error.HTTPError as e:
                print(f"Error asking question: {e.read().decode()}")

    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_chat()
