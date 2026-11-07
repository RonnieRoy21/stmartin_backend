import pyotp,os
from dotenv import load_dotenv


class PasswordGenerator:
    def __init__(self):
        load_dotenv()
        self.__secret = os.getenv("otp_secret")
        if not self.__secret:
            raise ValueError
        self.generator = pyotp.TOTP(s=self.__secret, interval=180)

    def generate_password(self):
        try:
            return self.generator.now()
        except Exception as e:
            print(f"Error generating code: {e.args}")
            raise

    def verify_password(self, code: str):
        try:
            return self.generator.verify(otp=code)
        except Exception as e:
            print(f"Error verifying code: {e.args}")
            raise
