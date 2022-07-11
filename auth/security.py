from time import time
from passlib.hash import pbkdf2_sha512
from pyotp import OTP, random_base32


class PasswordManager:
    """
    Main use for passlib can be found here:
    https://passlib.readthedocs.io/en/stable/index.html

    Using pbkdf2_sha512 has recommended here:
    https://passlib.readthedocs.io/en/stable/lib/passlib.hash.pbkdf2_digest.html
    """

    def compute_hash_password(self, password):
        return pbkdf2_sha512.hash(password)

    def verify_password(self, password, hashed_password):
        return pbkdf2_sha512.verify(password, hashed_password)


class OTPManager:
    """
    OTP implementation can be found here as it is not documented else where
    https://github.com/pyauth/pyotp/blob/develop/src/pyotp/otp.py

    s -> secret
    input -> Unix timestamp -> time.time()
    """
    def generate_otp(self):
        return OTP(s=random_base32()).generate_otp(input=int(time()))
