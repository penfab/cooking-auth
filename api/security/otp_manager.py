from time import time
from pyotp import OTP, random_base32

from api.config import BaseConfig


class OTPManager:
    """
    OTP source code implementation can be found here as it is not documented
    else where https://github.com/pyauth/pyotp/blob/develop/src/pyotp/otp.py

    s: str -> secret, random string
    input: int -> Unix timestamp -> int(time.time())
    """

    @classmethod
    def generate_otp(cls):
        otp = OTP(s=random_base32()).generate_otp(input=int(time()))
        return otp
