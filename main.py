import json
import logging

import requests
from flask import Flask, jsonify, request

from config import (
    SMS_GATEWAY_BASE_URL,
    SMS_GATEWAY_PASSWORD,
    SMS_GATEWAY_USER,
    WEBHOOK_EVENT,
    WEBHOOK_ID,
    WEBHOOK_PORT,
)
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


def ensure_webhook_registered():
    webhook_url = f"http://127.0.0.1:{WEBHOOK_PORT}/webhook"
    webhooks_endpoint = f"{SMS_GATEWAY_BASE_URL}/webhooks"
    
    try:
        response = requests.get(
            webhooks_endpoint,
            auth=(SMS_GATEWAY_USER, SMS_GATEWAY_PASSWORD),
            timeout=10,
        )
        response.raise_for_status()
        existing = response.json()
        
        webhook_exists = any(
            wh.get("id") == WEBHOOK_ID and wh.get("url") == webhook_url
            for wh in existing
        )
        
        if webhook_exists:
            logger.info("Webhook deja enregistre: %s", WEBHOOK_ID)
            return
        
        logger.info("Enregistrement du webhook: %s", WEBHOOK_ID)
        response = requests.post(
            webhooks_endpoint,
            json={"id": WEBHOOK_ID, "url": webhook_url, "event": WEBHOOK_EVENT},
            auth=(SMS_GATEWAY_USER, SMS_GATEWAY_PASSWORD),
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        response.raise_for_status()
        logger.info("Webhook enregistre avec succes")
        
    except requests.RequestException as exc:
        logger.error("Erreur gestion webhook: %s", exc)


if __name__ == "__main__":
    logger.info("Demarrage du serveur webhook sur le port %d", WEBHOOK_PORT)
    ensure_webhook_registered()
    app.run(host="127.0.0.1", port=WEBHOOK_PORT)
