from mailjet_rest import Client

from app.schema import EmailSchema
from config import settings


async def simple_send(subject: str, email: EmailSchema, token: str):
    html = f'<body><p> Please click following link to verify email </p><a target="_blank" href="{settings.APP_URL}/api/auth/verify/{token}">link</a></body>'

    api_key = settings.MAIL_API_KEY
    api_secret = settings.MAIL_API_SECRET
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "ek0519@gmail.com",
                    "Name": "Ekman"
                },
                "To": [
                    {
                        "Email": email,
                        "Name": 'New Member'
                    }
                ],
                "Subject": subject,
                "TextPart": "My first Mailjet email",
                "HTMLPart": html,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result
    # message = MessageSchema(
    #     subject=subject,
    #     recipients=email,
    #     template_body={"token": token, "url": settings.APP_URL}
    # )
    #
    # fm = FastMail(conf)
    # await fm.send_message(message, template_name="verify.html")
    # return True
