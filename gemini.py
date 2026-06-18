from google import genai
from google.genai import types
from .config import Config

_client = None


def get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=Config.GEMINI_API_KEY)
    return _client


SYSTEM_INSTRUCTION = (
    "You are a helpful WhatsApp assistant. "
    "Keep your replies concise and conversational. "
    "Avoid markdown formatting — plain text only."
)


def generate_reply(user_message: str) -> str:
    client = get_client()
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            max_output_tokens=8192,
        ),
    )
    return response.text.strip()
