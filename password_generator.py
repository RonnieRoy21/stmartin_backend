import pyotp

_secret = pyotp.random_base32(length=128)


class PasswordGenerator:
    def __init__(self):
        self.__secret = _secret
        self.generator = pyotp.TOTP(s=self.__secret, interval=120)

    def generate_password(self):
        try:
            return self.generator.now()
        except Exception as e:
            print(f"Error generating code: {e.args}")
            raise

    def verify_password(self, code: str):
        try:
            if self.generator.verify(otp=code):
                print("Verified")
                return
            print("Invalid Code")
        except Exception as e:
            print(f"Error verifying code: {e.args}")
            raise
