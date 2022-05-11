from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.schema import EmailSchema
from config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates"
)


async def simple_send(subject: str, email: EmailSchema, token: str):
    message = MessageSchema(
        subject=subject,
        recipients=email,
        template_body={"token": token, "url": settings.APP_URL}
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="verify.html")
    return True
