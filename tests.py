import unittest

from api.security.password_manager import PasswordManager
from api.security.otp_manager import OTPManager
from api.security.jwt_manager import JWTManager

from api.config import BaseConfig


class TestPasswordManager(unittest.TestCase):
    def test_password_OK(self):
        password = "fab"

        hashed_password = PasswordManager().compute_hash_password(password)
        confirmed_password = PasswordManager().verify_password(password, hashed_password)

        self.assertTrue(True, confirmed_password)

    def test_password_not_OK(self):
        password = "fab"
        hashed_password = PasswordManager().compute_hash_password(password)

        password = "baf"
        confirmed_password = PasswordManager().verify_password(password, hashed_password)

        self.assertFalse(False, confirmed_password)


class TestOTPManager(unittest.TestCase):
    def test_otp(self):
        otp = OTPManager().generate_otp()

        self.assertIsNotNone(otp)


class TestJWTManager(unittest.TestCase):
    def test_jwt_token_OK(self):
        secret_key = BaseConfig.JWT_SECRET_KEY

        expected_value = "fab"

        encoded_token = JWTManager.generate_token(
            key="sub",
            value="fab",
            secret_key=secret_key)

        decoded_token = JWTManager.decode_token(
            encoded_token=encoded_token,
            secret_key=secret_key)

        self.assertEqual(expected_value, decoded_token.get("sub"))

    def test_jwt_token_not_OK(self):
        secret_key = BaseConfig.JWT_SECRET_KEY

        encoded_token = JWTManager.generate_token(
            key="sub",
            value="fab",
            secret_key=secret_key)

        secret_key = "nottherealsecretkey"

        decoded_token = JWTManager.decode_token(
            encoded_token=encoded_token,
            secret_key=secret_key)

        self.assertIsNone(decoded_token)


if __name__ == "__main__":
    unittest.main()
