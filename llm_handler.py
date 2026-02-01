"""
LLM handler - handles Q&A using OpenAI or Claude API
"""
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', ''))

def answer_question(question, context, max_tokens=500):
    """
    Answer a question based on PDF context using OpenAI API
    
    Args:
        question: User's question/doubt
        context: PDF content as context
        max_tokens: Max response length
    
    Returns:
        Answer string
    """
    try:
        if not os.getenv('OPENAI_API_KEY'):
            return "LLM not configured. Set OPENAI_API_KEY environment variable to enable Q&A."
        
        # Truncate context to avoid token limits
        context_truncated = context[:3000] if len(context) > 3000 else context
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert educational assistant. Answer questions based on the provided module content. If the answer is not in the content, say so clearly."
                },
                {
                    "role": "user",
                    "content": f"Module Content:\n{context_truncated}\n\nQuestion: {question}"
                }
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error: Unable to generate answer. {str(e)}"
