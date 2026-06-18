import logging
from flask import Blueprint, request, jsonify
from .config import Config
from .gemini import generate_reply
from .whatsapp import send_message

logger = logging.getLogger(__name__)

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == Config.WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return challenge, 200

    logger.warning("Webhook verification failed: invalid token or mode")
    return jsonify({"error": "Verification failed"}), 403


@webhook_bp.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    try:
        entry = data.get("entry", [])
        for item in entry:
            for change in item.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for msg in messages:
                    if msg.get("type") != "text":
                        continue
                    sender = msg["from"]
                    user_text = msg["text"]["body"]
                    logger.info("Message from %s: %s", sender, user_text)

                    reply = generate_reply(user_text)
                    send_message(sender, reply)
                    logger.info("Reply sent to %s", sender)

    except Exception as exc:
        logger.exception("Error processing webhook: %s", exc)
        return jsonify({"error": "Internal server error"}), 500

    return jsonify({"status": "ok"}), 200


@webhook_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200
