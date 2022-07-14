from datetime import datetime, timedelta

from jose.jwt import encode, decode
from jose.exceptions import JWTError

from api.config import BaseConfig


class JWTManager:
    """
    Based on the official example found at https://pypi.org/project/python-jose/
    Will use HS512 algorithm as the only option instead of HS256
    """

    @classmethod
    def generate_token(cls, key, value, secret_key):
        expires_in = datetime.utcnow() + timedelta(seconds=BaseConfig.JWT_EXPIRES_IN_SECONDS)
        encoded_token = encode(
            {f"{key}": f"{value}", "exp": expires_in},
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
