import json
import logging

from flask import Flask, jsonify, request

from config import WEBHOOK_PORT
from router import route_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def extract_webhook_data(data):
    if not isinstance(data, dict):
        return None, None

    payload = data.get("payload", data)
    phone = payload.get("phoneNumber")
    message = payload.get("message")
    return phone, message


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    logger.info("Webhook recu: %s", json.dumps(data, ensure_ascii=False))

    phone, body = extract_webhook_data(data)

    if not phone or not body:
        logger.warning("Webhook ignore: donnees manquantes")
        return jsonify({"status": "ignored", "reason": "missing data"}), 400

    route_message(phone, body)
    return jsonify({"status": "ok"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"}), 200


if __name__ == "__main__":
    logger.info("Demarrage du serveur webhook sur le port %d", WEBHOOK_PORT)
    app.run(host="127.0.0.1", port=WEBHOOK_PORT)
