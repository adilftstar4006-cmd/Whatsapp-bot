import os


class Config:
    WHATSAPP_ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN", "")
    WHATSAPP_PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID", "")
    WHATSAPP_VERIFY_TOKEN = os.environ.get("WHATSAPP_VERIFY_TOKEN", "")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    WHATSAPP_API_URL = (
        f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    )

    @classmethod
    def validate(cls):
        missing = []
        for key in ("WHATSAPP_ACCESS_TOKEN", "WHATSAPP_PHONE_NUMBER_ID",
                    "WHATSAPP_VERIFY_TOKEN", "GEMINI_API_KEY"):
            if not getattr(cls, key):
                missing.append(key)
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
