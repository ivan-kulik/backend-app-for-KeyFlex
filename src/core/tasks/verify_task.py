import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr

from core.config import settings


def get_email_message_template(
    user_email: EmailStr,
    token: str,
) -> MIMEMultipart:
    msg: MIMEMultipart = MIMEMultipart()
    msg["From"] = settings.email_verification.SMTP_USER
    msg["To"] = user_email
    msg["Subject"] = settings.email_verification.msg_subject

    env = Environment(loader=FileSystemLoader("core/templates/email_verification"))
    template = env.get_template("email_message.html")

    html_content = template.render(
        msg_subtitle_text=settings.email_verification.msg_subtitle_text,
        msg_paragraph1_text=settings.email_verification.msg_paragraph1_text,
        msg_paragraph2_text=settings.email_verification.msg_paragraph2_text,
        url_link=f"{settings.email_verification.url_link}{token}",
        msg_confirm_button_text=settings.email_verification.msg_confirm_button_text,
    )
    msg.attach(MIMEText(html_content, "html"))
    return msg


def send_email_message_to_verify_email(
    user_email: EmailStr,
    token: str,
) -> None:
    email_message: MIMEMultipart = get_email_message_template(
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
