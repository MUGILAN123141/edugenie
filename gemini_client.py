from functools import lru_cache
from google import genai
from config import settings

@lru_cache(maxsize=1)
def get_client():
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add it to your .env file."
        )
    return genai.Client(api_key=settings.gemini_api_key)

def generate_text(prompt: str, *, system_instruction: str | None = None) -> str:
    client = get_client()
    config = {}
    if system_instruction:
        config["system_instruction"] = system_instruction
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config or None,
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()

def generate_structured(prompt: str, schema):
    client = get_client()
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": schema,
        },
    )
    parsed = getattr(response, "parsed", None)
    if parsed is not None:
        return parsed
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned no structured response.")
    return schema.model_validate_json(text)
