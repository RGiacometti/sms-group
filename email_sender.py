import logging
import smtplib
from email.message import EmailMessage

from config import MEMBRES, SMTP_FROM_EMAIL, SMTP_FROM_NAME, SMTP_PASSWORD, SMTP_PORT, SMTP_SERVER, SMTP_USER

logger = logging.getLogger(__name__)


def send_group_email(sender_name, message_text):
    msg = EmailMessage()
    msg["Subject"] = f"[Groupe SMS] Message de {sender_name}"
    msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
    msg["To"] = ", ".join(m["email"] for m in MEMBRES)
    msg.set_content(message_text)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        logger.info("Email envoye au groupe")
        return True
    except Exception as exc:
        logger.error("Erreur envoi email: %s", exc)
        return False
