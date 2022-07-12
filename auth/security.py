from subprocess import run, PIPE
from shlex import split
from time import time
from passlib.hash import pbkdf2_sha512
from pyotp import OTP, random_base32
from jose.jwt import encode, decode
from jose.exceptions import JWTError

from api.config import BaseConfig


class PasswordManager:
    """
    Main use for passlib can be found here:
    https://passlib.readthedocs.io/en/stable/index.html

    Using pbkdf2_sha512 has recommended here:
    https://passlib.readthedocs.io/en/stable/lib/passlib.hash.pbkdf2_digest.html
    """

    @classmethod
    def compute_hash_password(cls, password):
        return pbkdf2_sha512.hash(password)

    @classmethod
    def verify_password(cls, password, hashed_password):
        return pbkdf2_sha512.verify(password, hashed_password)


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


class JWTManager:
    """
    Based on the official example found at https://pypi.org/project/python-jose/
    Will use HS512 algorithm as the only option instead of HS256
    """

    @classmethod
    def generate_secret_key(cls):
        cmd = "openssl rand -hex 32" # documented on FastAPI
        secret_key = run(split(cmd), stdout=PIPE)
        return secret_key.stdout.decode("utf-8")


    @classmethod
    def generate_token(cls, key, value, secret_key):
        encoded_token = encode(
                {f"{key}": f"{value}"},
                secret_key,
                algorithm=BaseConfig.JWT_ALGORITHM)
        return encoded_token

    @classmethod
    def decode_token(cls, encoded_token, secret_key):
        try:
            decoded_token = decode(
                    encoded_token,
                    secret_key,
                    algorithms=BaseConfig.JWT_ALGORITHM)
            return decoded_token
        except JWTError as e:
            return
