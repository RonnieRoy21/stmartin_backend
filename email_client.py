import os
import requests

from dotenv import load_dotenv

from custom_response import CustomResponse
from password_generator import PasswordGenerator


class EmailClient:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("BREVO_API_KEY")
        self.sender = os.getenv("BREVO_SENDER")
        self.sender_name = os.getenv("BREVO_SENDER_NAME")

        self.host = "https://api.brevo.com/v3/smtp/email"

        self.headers = {
            "api-key": self.api_key,
            "accept": "application/json",
            "content-type": "application/json",
        }

    def send_otp_email(self, recipient_email: str):

        if not self.api_key or not self.sender:
            return CustomResponse(
                message="Server Error.", error="Unable to access Brevo Email Service."
            )

        try:
            gen = PasswordGenerator()
            ver_code = gen.generate_password()

            msg = f"""
Your Verification Code for St Martin Counsellors Admin Login is:

{ver_code}

The code EXPIRES IN 3 MINUTES.

If you did not request this code, you can safely ignore this email.

This email is auto-generated. Do not reply.

Thank you,
Fin Technologies ICT Team.
"""

            payload = {
                "sender": {"name": self.sender_name, "email": self.sender},
                "to": [{"email": recipient_email}],
                "subject": "Admin Verification",
                "textContent": msg,
                "replyTo": {"email": self.sender, "name": self.sender_name},
            }

            response = requests.post(
                self.host, headers=self.headers, json=payload, timeout=15
            )

            response.raise_for_status()

            return CustomResponse(
                message=(
                    f"An email has been sent by {self.sender}. "
                    "Check your inbox and spam folder if necessary."
                )
            )

        except requests.exceptions.Timeout:
            return CustomResponse(
                message="Email Service Timeout.", error="Brevo did not respond in time."
            )

        except requests.exceptions.HTTPError as he:
            assert he.response is not None
            print(f"Brevo HTTP Error: {he.response.status_code}")
            print(f"Brevo Response: {he.response.text}")

            return CustomResponse(
                message="Error Occurred.", error="Failed to send OTP."
            )

        except requests.exceptions.RequestException as re:
            print(f"Brevo Connection Error: {re}")

            return CustomResponse(
                message="Error Occurred.", error="Unable to connect to Brevo."
            )

        except Exception as e:
            print(f"Unexpected Email Error: {e}")

            return CustomResponse(
                message="Error Occurred.", error="Failed to send OTP."
            )
