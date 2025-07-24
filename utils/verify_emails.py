# app/email_utils.py
import smtplib
from email.mime.text import MIMEText
from config.user import settings

def send_verification_email(email: str, token: str):
    msg = MIMEText(f"Click to verify your email: http://localhost:8000/verify-email?token={token}")
    msg['Subject'] = "Verify your email"
    msg['From'] = settings.SMTP_EMAIL
    msg['To'] = email

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_EMAIL, email, msg.as_string())

