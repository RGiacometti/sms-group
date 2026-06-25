import logging

import requests

from config import SMS_GATEWAY_PASSWORD, SMS_GATEWAY_URL, SMS_GATEWAY_USER

logger = logging.getLogger(__name__)


def broadcast_sms(recipients, text):
    phone_numbers = [m["phone"] for m in recipients]
    try:
        response = requests.post(
            SMS_GATEWAY_URL,
            json={"textMessage": {"text": text}, "phoneNumbers": phone_numbers},
            auth=(SMS_GATEWAY_USER, SMS_GATEWAY_PASSWORD),
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        response.raise_for_status()
        logger.info("SMS envoye a %d destinataires", len(phone_numbers))
        return len(phone_numbers)
    except requests.RequestException as exc:
        logger.error("Erreur envoi SMS: %s", exc)
        return 0
