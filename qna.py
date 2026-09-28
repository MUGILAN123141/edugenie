from gemini_client import generate_text

def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, a student-friendly academic assistant.
Answer the question accurately and concisely.

Question:
{question}

Rules:
- Explain in simple language.
- Use short paragraphs or bullets when useful.
- If the question is ambiguous, state the assumption you made.
- Do not invent citations or sources.
"""
    return generate_text(prompt)
