import logging

import requests

from config import SMS_GATEWAY_TOKEN, SMS_GATEWAY_URL

logger = logging.getLogger(__name__)


def send_sms(phone, text):
    try:
        response = requests.post(
            SMS_GATEWAY_URL,
            json={"address": phone, "textBody": text},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {SMS_GATEWAY_TOKEN}",
            },
            timeout=30,
        )
        response.raise_for_status()
        logger.info("SMS envoye a %s", phone)
        return True
    except requests.RequestException as exc:
        logger.error("Erreur envoi SMS a %s: %s", phone, exc)
        return False


def broadcast_sms(recipients, text):
    success_count = 0
    for member in recipients:
        if send_sms(member["phone"], text):
            success_count += 1
    return success_count
