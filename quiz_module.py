from gemini_client import generate_structured
from schemas import QuizResult

def generate_quiz(topic: str, count: int = 5, level: str = "beginner") -> QuizResult:
    prompt = f"""
Create a {count}-question multiple-choice quiz about "{topic}" for a {level} learner.

Requirements:
- Exactly {count} questions.
- Exactly four options per question.
- correct_answer must exactly match one option.
- Include a short explanation for every answer.
- Questions should test understanding, not only memorization.
- Return only data matching the supplied schema.
"""
    result = generate_structured(prompt, QuizResult)
    # The model may omit the topic value; normalize it for the API contract.
    result.topic = topic
    return result
