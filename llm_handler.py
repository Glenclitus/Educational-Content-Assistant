"""
LLM handler - handles Q&A using OpenAI API via direct HTTP requests
Includes Local Fallback Mode (No API)
"""
import os
import json
import requests
import random

def answer_question(question, context, max_tokens=500):
    """
    Answer a question based on PDF context.
    Uses OpenAI API if key is present, otherwise falls back to local keyword search.
    """
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        
        # --- LOCAL FALLBACK MODE (No API Key) ---
        if not api_key:
            print("Using Local Keyword Search Mode (No API Key provided)")
            
            # Simple keyword-based extraction
            paragraphs = [p.strip() for p in context.split('\n\n') if p.strip()]
            if not paragraphs:
                return "I couldn't find any content in this module to search."

            # Remove punctuation and lowercase
            q_words = set(word.lower().strip('?,.! ') for word in question.split())
            if not q_words:
                return "Please ask a question containing words found in the document."

            best_match = None
            max_score = 0

            for para in paragraphs:
                para_lower = para.lower()
                # Calculate score: number of question words present in paragraph
                score = sum(1 for word in q_words if word in para_lower)
                
                # Boost score for exact phrase matches
                if question.lower().strip('?') in para_lower:
                    score += 5
                
                if score > max_score:
                    max_score = score
                    best_match = para

            if max_score > 0 and best_match:
                return f"[Local Search Result] Found in document:\n\n{best_match}\n\n(Note: Using keyword search mode because no API key is configured.)"
            else:
                return f"I couldn't find a specific answer to \"{question}\" in the text using keyword search."
        # --- END LOCAL FALLBACK ---

        # Truncate context to avoid token limits
        context_truncated = context[:3000] if len(context) > 3000 else context
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-3.5-turbo", 
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert educational assistant. Answer based on context."
                },
                {
                    "role": "user",
                    "content": f"Module Content:\n{context_truncated}\n\nQuestion: {question}"
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        if base_url.endswith('/'):
            base_url = base_url[:-1]
            
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            return f"Error from OpenAI API: {response.status_code} - {response.text}"
            
        data = response.json()
        return data['choices'][0]['message']['content']
    
    except Exception as e:
        return f"Error generating answer: {str(e)}"

def generate_mcqs(content, count=5):
    """
    Generate MCQ questions from content.
    Uses OpenAI API if present, otherwise generates pseudo-MCQs locally.
    """
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        
        if not api_key:
            # Generate pseudo-MCQs locally
            sentences = [s.strip() for s in content.replace('!', '.').replace('?', '.').split('.') if len(s.strip()) > 50]
            
            local_mcqs = []
            if len(sentences) >= count:
                selected_sentences = random.sample(sentences, min(count, len(sentences)))
                
                for i, sent in enumerate(selected_sentences):
                    # Create a "Verify this statement" style MCQ
                    local_mcqs.append({
                        "question": f"Is this statement found in the text: \"{sent[:100]}...\"?",
                        "options": ["Yes", "No", "Maybe", "Unknown"],
                        "correct": "A",
                        "difficulty": "easy",
                        "explanation": "This sentence is present in the document."
                    })
            
            if local_mcqs:
                return local_mcqs
            
            return [{
                "question": "What does this module primarily cover?",
                "options": ["The uploaded PDF content", "General Knowledge", "Math", "Science"],
                "correct": "A",
                "difficulty": "easy",
                "explanation": "This module covers the content of the uploaded PDF."
            }]
        
        # API Implementation
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        content_truncated = content[:2500] if len(content) > 2500 else content
        prompt = f"Generate {count} MCQs from this content in JSON format."

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a quiz generator. Return only JSON."},
                {"role": "user", "content": f"Content:\n{content_truncated}\n\nTask: Generate {count} MCQs with 'question','options','correct','difficulty','explanation'. Return only JSON list."}
            ],
            "max_tokens": 1500
        }
        
        if base_url.endswith('/'):
            base_url = base_url[:-1]

        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=45
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return []
            
        result_text = response.json()['choices'][0]['message']['content'].strip()
        
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(result_text)
    
    except Exception as e:
        print(f"MCQ Error: {e}")
        return []
