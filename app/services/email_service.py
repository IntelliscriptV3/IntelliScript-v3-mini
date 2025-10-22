from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from ..core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USERNAME,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_invite_email(to: str, username: str, temp_password: str):
    fm = FastMail(conf)
    msg = MessageSchema(
        subject="Your IntelliScript Instructor Account",
        recipients=[to],
        body=f"Hello,\n\nYour instructor account has been created.\nUsername: {username}\nTemporary password: {temp_password}\n\nPlease log in and change it.\n",
        subtype="plain",
    )
    await fm.send_message(msg)
