import requests
from .config import Config


def send_message(to: str, text: str) -> dict:
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    url = (
        f"https://graph.facebook.com/v19.0/"
        f"{Config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    )
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()
