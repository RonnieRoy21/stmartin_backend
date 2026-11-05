import os
import smtplib
import ssl
from email.message import EmailMessage
from smtplib import (
    SMTPAuthenticationError,
    SMTPConnectError,
    SMTPSenderRefused,
    SMTPServerDisconnected,
)

from dotenv import load_dotenv

from custom_response import CustomResponse
from password_generator import PasswordGenerator


class EmailClient:
    def __init__(self):
        load_dotenv()
        self.message = EmailMessage()
        self.port = 587
        self.host = "smtp.gmail.com"
        self.sender = os.getenv("sender_email")
        self.password = os.getenv("sender_password")

    def send_otp_email(self, recipient_email: str):
        if not self.sender or not self.password:
                return CustomResponse(
                    message="Server Error.", error="Unable to reach Email Server"
                )
        try:
            gen=PasswordGenerator()
            ver_code=gen.generate_password()

            msg: str = f"""
            Your Verification Code for St Martin Admin Login is {ver_code}.

            The code EXPIRES IN 2 MINUTES.

            If you did not request the code you can safely ignore this email.

            This Email is auto-generated.Do not reply.

            Thank you,
            St Martin ICT Team.
"""

            with smtplib.SMTP(host=self.host, port=self.port) as server:
                ctx = ssl.create_default_context()
                server.ehlo()
                server.starttls(context=ctx)
                server.ehlo()
                server.login(user=self.sender, password=self.password)
                self.message["To"] = recipient_email
                self.message["From"] = self.sender
                self.message["Subject"] = "Admin Verification"

                self.message.set_content(msg)
                server.send_message(self.message)
                return CustomResponse(
                    message=f"An email has been sent by {self.sender}.Check your Email inbox and spam folder if necessary."
                )
        except SMTPConnectError as ce:
            print(f"Error sending email: {ce.winerror}")
            print(f"Error sending email: {ce.filename}")
            print(f"Error sending email: {ce.args[0]}")
            return CustomResponse(message="Error Occured", error="Failed to send OTP")
        except SMTPServerDisconnected as sd:
            print(f"Server Disconnected: {sd.args[0]}")
        except SMTPSenderRefused as sr:
            print(f"Sender refused :{sr.args}")
        except SMTPAuthenticationError as ae:
            print(f"Authentication Error: {ae.args}")
