from gemini_client import generate_text

def recommend_learning_path(topic: str, level: str, goal: str) -> str:
    prompt = f"""
Design a practical learning path for the topic "{topic}".
Learner level: {level}
Goal: {goal}

Return:
1. Prerequisites
2. A sequence of 5-7 learning stages from the learner's current level toward the goal
3. A small practice activity for each stage
4. Suggested self-check questions
5. A final project or mastery task

Keep it concise and student-friendly.
"""
    return generate_text(prompt)
