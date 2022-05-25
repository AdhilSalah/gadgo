
from django.conf import settings
from twilio.rest import Client
import random


class MessageHandler:

    phone_number = None
    otp = None

    def __init__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp = otp

    def send_otp_on_phone(self):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

        message = client.messages.create(
            from_='+12057975634',
            body=f'your otp is{self.otp}',
            to=self.phone_number
        )

        print(message.sid)
