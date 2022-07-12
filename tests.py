import unittest

from auth.security import PasswordManager, OTPManager, JWTManager


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
        secret_key = JWTManager.generate_secret_key()

        expected_value = {"fab": "baf"}

        encoded_token = JWTManager.generate_token(
                key="fab",
                value="baf",
                secret_key=secret_key)

        decoded_token = JWTManager.decode_token(
                encoded_token=encoded_token,
                secret_key=secret_key)

        self.assertEqual(expected_value, decoded_token)

    def test_jwt_token_not_OK(self):
        secret_key = JWTManager.generate_secret_key()

        expected_value = {"hello": "world"}

        encoded_token = JWTManager.generate_token(
                key="hello",
                value="world",
                secret_key=secret_key)

        secret_key+= "1"

        decoded_token = JWTManager.decode_token(
                encoded_token=encoded_token,
                secret_key=secret_key)

        self.assertNotEqual(expected_value, decoded_token)


if __name__ == "__main__":
    unittest.main()
