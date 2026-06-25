import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SMS_GATEWAY_URL = os.getenv("SMS_GATEWAY_URL", "http://127.0.0.1:8080/message")
SMS_GATEWAY_USER = os.getenv("SMS_GATEWAY_USER", "")
SMS_GATEWAY_PASSWORD = os.getenv("SMS_GATEWAY_PASSWORD", "")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "5000"))

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Groupe SMS")
SMTP_FROM_EMAIL = SMTP_USER

SMS_MAX_LENGTH = 160
SMS_TRUNCATE_LENGTH = 120

membres_path = Path(__file__).parent / "membres.json"
MEMBRES = json.loads(membres_path.read_text(encoding="utf-8"))


def normalize_phone(phone):
    if not phone:
        return ""
    phone = phone.replace(" ", "").replace("-", "").replace(".", "")
    if phone.startswith("00"):
        phone = "+" + phone[2:]
    if phone.startswith("0") and len(phone) == 10:
        phone = "+33" + phone[1:]
    return phone


def find_member_by_phone(phone):
    normalized = normalize_phone(phone)
    for member in MEMBRES:
        if normalize_phone(member["phone"]) == normalized:
            return member
    return None


def get_recipients(exclude_phone):
    normalized = normalize_phone(exclude_phone)
    return [m for m in MEMBRES if normalize_phone(m["phone"]) != normalized]
