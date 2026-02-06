"""
LLM handler - handles Q&A using OpenAI or Claude API
"""
import os
import json

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
            # Return a mock answer if no API key is set
            return f"""Based on the provided content, here's an answer to your question: "{question}"
            
This is a demo response. To enable real AI-powered answers, please set the OPENAI_API_KEY environment variable with your OpenAI API key.

In a production environment with LLM enabled, this would provide a detailed, contextual answer based on your module content."""
        
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
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
        return f"Demo response: Unable to generate AI answer at this moment. {str(e)}"

def generate_mcqs(content, count=5):
    """
    Generate MCQ questions from content
    
    Args:
        content: Study material content
        count: Number of MCQs to generate
    
    Returns:
        List of MCQ dictionaries
    """
    try:
        if not os.getenv('OPENAI_API_KEY'):
            # Return demo MCQs if no API key
            return [
                {
                    "question": "What is the main topic discussed in this module?",
                    "options": [
                        "Educational concepts",
                        "Advanced mathematics",
                        "Historical events",
                        "Scientific principles"
                    ],
                    "correct": "A",
                    "difficulty": "easy",
                    "explanation": "The content focuses on educational concepts and learning."
                },
                {
                    "question": "Which approach is most effective for studying?",
                    "options": [
                        "Passive reading only",
                        "Active recall and practice",
                        "Memorization without understanding",
                        "Skipping difficult topics"
                    ],
                    "correct": "B",
                    "difficulty": "medium",
                    "explanation": "Active recall and practice lead to better retention."
                }
            ]
        
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Truncate content
        content_truncated = content[:2500] if len(content) > 2500 else content
        
        prompt = f"""You are an expert tutor. Generate {count} multiple-choice questions from this content:

{content_truncated}

Requirements:
- Mix difficulty levels (easy, medium, hard)
- 4 options per question
- Include correct answer (A, B, C, or D)
- Add brief explanation

Return ONLY a valid JSON array with this exact structure:
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": "A",
    "difficulty": "easy",
    "explanation": "Brief explanation"
  }}
]

Return ONLY the JSON array, no other text."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert educational content creator. You generate MCQs in valid JSON format only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1500,
            temperature=0.8
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Try to extract JSON if wrapped in code blocks
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        questions = json.loads(result_text)
        return questions
    
    except Exception as e:
        print(f"MCQ generation error: {e}")
        # Return fallback MCQs
        return [
            {
                "question": "What is the key concept from this study material?",
                "options": [
                    "Understanding the fundamentals",
                    "Skipping the basics",
                    "Ignoring context",
                    "Random memorization"
                ],
                "correct": "A",
                "difficulty": "easy",
                "explanation": "Understanding fundamentals is crucial for learning."
            }
        ]
