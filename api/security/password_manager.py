from passlib.hash import pbkdf2_sha512

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
