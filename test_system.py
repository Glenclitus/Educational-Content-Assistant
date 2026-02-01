"""
Test script to verify the Educational Content Assistant is working end-to-end
"""
import requests
import json
import sqlite3
import time

API_URL = 'http://127.0.0.1:5000/api'

def test_health():
    """Test API health endpoint"""
    print("Testing API health...")
    time.sleep(1)  # Give backend time to respond
    try:
        response = requests.get(f'{API_URL}/health', timeout=5)
        print(f"✅ API Health: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ API Health Check Failed: {e}")
        return False

def test_get_modules():
    """Get list of uploaded modules"""
    print("\nFetching uploaded modules...")
    try:
        response = requests.get(f'{API_URL}/modules')
        modules = response.json().get('modules', [])
        print(f"✅ Found {len(modules)} module(s)")
        for mod in modules:
            print(f"   - {mod['module_name']} (ID: {mod['id']}, Uploaded: {mod['upload_date']})")
        return modules
    except Exception as e:
        print(f"❌ Failed to fetch modules: {e}")
        return []

def test_ask_question(pdf_id):
    """Test asking a question"""
    print(f"\nTesting Q&A for module ID {pdf_id}...")
    
    question = "What is the main topic of this document?"
    
    try:
        response = requests.post(
            f'{API_URL}/ask',
            json={'pdf_id': pdf_id, 'question': question}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Question submitted successfully")
            print(f"   Question: {result.get('question')}")
            print(f"   Answer: {result.get('answer')[:100]}...")
            return True
        else:
            print(f"❌ Question failed with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Question failed: {e}")
        return False

def test_get_conversations(pdf_id):
    """Get conversation history"""
    print(f"\nFetching conversation history for module ID {pdf_id}...")
    try:
        response = requests.get(f'{API_URL}/conversations/{pdf_id}')
        conversations = response.json().get('conversations', [])
        print(f"✅ Found {len(conversations)} conversation(s)")
        for i, conv in enumerate(conversations, 1):
            print(f"   Q{i}: {conv['question'][:50]}...")
            print(f"   A{i}: {conv['answer'][:50]}...")
        return True
    except Exception as e:
        print(f"❌ Failed to fetch conversations: {e}")
        return False

def test_database():
    """Check database directly"""
    print("\nChecking database...")
    try:
        conn = sqlite3.connect('assistant.db')
        c = conn.cursor()
        
        # Check PDFs table
        c.execute('SELECT COUNT(*) FROM pdfs')
        pdf_count = c.fetchone()[0]
        print(f"✅ Database PDFs: {pdf_count}")
        
        # Check conversations table
        c.execute('SELECT COUNT(*) FROM conversations')
        conv_count = c.fetchone()[0]
        print(f"✅ Database Conversations: {conv_count}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Educational Content Assistant - System Test")
    print("=" * 60)
    
    # Run tests
    if not test_health():
        print("\n⚠️  Backend is not running. Start with: python app.py")
        exit(1)
    
    test_database()
    modules = test_get_modules()
    
    if modules:
        module_id = modules[0]['id']
        test_ask_question(module_id)
        test_get_conversations(module_id)
    else:
        print("\n⚠️  No modules found. Upload a PDF first through the website.")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
