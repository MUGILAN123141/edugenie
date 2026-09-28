from gemini_client import generate_text

def summarize_text(text: str, level: str = "beginner") -> str:
    prompt = f"""
Summarize the following educational passage for a {level} learner.

Keep the main ideas, important facts, relationships, and conclusions.
Remove repetition and unnecessary detail.
Use clear bullets when they improve readability.

PASSAGE:
{text}
"""
    return generate_text(prompt)
