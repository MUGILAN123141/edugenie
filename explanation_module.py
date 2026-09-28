from gemini_client import generate_text
from config import settings

_local_pipeline = None

def _get_local_pipeline():
    global _local_pipeline
    if _local_pipeline is None:
        try:
            from transformers import pipeline
            _local_pipeline = pipeline(
                "text2text-generation",
                model=settings.local_explanation_model,
            )
        except Exception as exc:
            raise RuntimeError(
                "Local explanation model could not be loaded. "
                "Install requirements-local.txt or set ENABLE_LOCAL_EXPLANATION=false."
            ) from exc
    return _local_pipeline

def explain_topic(topic: str, level: str = "beginner") -> str:
    prompt = (
        f"Explain {topic} to a {level} learner. "
        "Use a simple definition, key points, a small example, and a short recap."
    )
    if settings.enable_local_explanation:
        try:
            pipe = _get_local_pipeline()
            result = pipe(prompt, max_new_tokens=300, do_sample=False)
            return result[0]["generated_text"].strip()
        except Exception:
            # Cloud fallback keeps the web app usable if local inference fails.
            pass
    return generate_text(prompt)
