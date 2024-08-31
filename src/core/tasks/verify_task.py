import smtplib
from email.message import EmailMessage
from pydantic import EmailStr

from core.config import settings


def get_email_message_template(username: str, user_email: EmailStr, token: str):
    email = EmailMessage()
    email["Subject"] = "Подтверждение электронной почты"
    email["From"] = settings.email_verification.SMTP_USER
    email["To"] = user_email

    url = f"https://keyflex.netlify.app/profile?token={token}"

    email.set_content(
        "<div>"
        f"<h3>Здравствуйте, {username}. Перейдите по данной ссылке для подтверждения вашей почты: {url}</h3>"
        "</div>",
        subtype="html",
    )
    return email


def send_email_message_to_verify_email(
    username: str,
    user_email: EmailStr,
    token: str,
):
    email_message = get_email_message_template(
        username=username,
        user_email=user_email,
        token=token,
    )

    with smtplib.SMTP_SSL(
        settings.email_verification.SMTP_HOST,
        settings.email_verification.SMTP_PORT,
    ) as server:
        server.login(
            settings.email_verification.SMTP_USER,
            settings.email_verification.SMTP_PASSWORD,
        )
        server.send_message(email_message)
