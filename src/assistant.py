"""Simple CLI starter for Educational Content Assistant

This script provides template-based content generation locally.
It does NOT call an LLM by default; instructions included for integration.
"""
import argparse
import os

TEMPLATE = {
    'lesson': """
Lesson: {title}
Level: {level}
Objectives:
- Understand the main idea
- Explore examples

Summary:
{summary}

Practice Questions:
1. {q1}
2. {q2}
""",
}


def generate_lesson(topic, level):
    # Lightweight placeholder generator — replace with LLM calls
    summary = f"A concise summary of {topic} at {level} level."
    q1 = f"Explain the core idea of {topic}."
    q2 = f"Give an example where {topic} applies."
    return TEMPLATE['lesson'].format(title=topic, level=level, summary=summary, q1=q1, q2=q2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Educational Content Assistant CLI')
    parser.add_argument('--topic', required=True, help='Topic to generate content for')
    parser.add_argument('--level', default='beginner', choices=['beginner', 'intermediate', 'advanced'])
    args = parser.parse_args()

    lesson = generate_lesson(args.topic, args.level)
    print(lesson)

    # Optional: integrate LLM by checking environment variable
    api_key = os.getenv('LLM_API_KEY')
    if api_key:
        print('\nLLM integration is enabled (LLM_API_KEY found). Update src/assistant.py to call your provider.')
    else:
        print('\nNo LLM API key found. To enable, set environment variable LLM_API_KEY.')
