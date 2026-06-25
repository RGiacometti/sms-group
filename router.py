import logging

from config import SMS_MAX_LENGTH, SMS_TRUNCATE_LENGTH, find_member_by_phone, get_recipients
from email_sender import send_group_email
from sms_sender import broadcast_sms

logger = logging.getLogger(__name__)


def route_message(sender_phone, message_text):
    sender = find_member_by_phone(sender_phone)
    if not sender:
        logger.warning("Expediteur non autorise ignore: %s", sender_phone)
        return False

    logger.info(
        "Message de %s (%s), %d caracteres",
        sender["name"],
        sender["phone"],
        len(message_text),
    )

    recipients = get_recipients(sender_phone)

    if len(message_text) <= SMS_MAX_LENGTH:
        sms_text = f"{sender['name']} : {message_text}"
        logger.info("Distribution SMS (message court)")
        success = broadcast_sms(recipients, sms_text)
        logger.info("SMS envoyes a %d/%d destinataires", success, len(recipients))
    else:
        truncated = message_text[:SMS_TRUNCATE_LENGTH]
        sms_text = f"{sender['name']} : {truncated}... [Suite recue par Email]"
        logger.info("Distribution SMS tronque + Email (message long)")
        success = broadcast_sms(recipients, sms_text)
        logger.info("SMS tronques envoyes a %d/%d destinataires", success, len(recipients))

        if not send_group_email(sender["name"], message_text):
            logger.error("Echec envoi email - SMS tronque tout de meme distribue")

    return True
