import unittest
import json
from datetime import datetime
from httpx import AsyncClient

from api.main import serve_api, mongo_client, redis_client
from api.databases.redis import redis_set_key
from api.user import User

from api.security.password_manager import PasswordManager
from api.security.otp_manager import OTPManager
from api.security.jwt_manager import JWTManager

from api.config import BaseConfig


api = serve_api()


class TestAPI(unittest.IsolatedAsyncioTestCase):
    async def test_register(self):
        data = {'username': "fab",
                'email': 'fab@baf.com',
                'password': 123,
                'gender': 'M',
                'cooker': False,
                'enable_2fa': False,
                'verified_otp': False,
                'joined_on': datetime.now()}

        async with AsyncClient(app=api, base_url="http://test") as ac:
            response = await ac.post(
                "/register",
                params=data)

        # redirection -> logged in after registration
        assert response.status_code == 302


    async def test_register_with_2fa(self):
        # user can't be redirected as OTP needs to be verified
        data = {'username': "fab1",
                'email': 'fab1@baf.com',
                'password': 123,
                'gender': 'M',
                'cooker': False,
                'enable_2fa': True,
                'verified_otp': False,
                'joined_on': datetime.now()}

        async with AsyncClient(app=api, base_url="http://test") as ac:
            response = await ac.post(
                "/register",
                params=data)

        response = response.json()
        assert response == {'message': "we sent you a verification code to 'fab1@baf.com'"}


    async def test_virify_2fa_with_wrong_otp(self):
        # verify with a fake OTP
        data = {"email": "fab1@baf.com", "verified_otp": "000000"}
        async with AsyncClient(app=api, base_url="http://test") as ac:
            response = await ac.post(
                "/verify_otp",
                params=data)

        response = response.json()

        # email/otp does not match
        assert response == {'message': 'verification code has expired'}


    async def test_virify_2fa_with_verified_otp(self):
        email = "fab1@baf.com"

        # overright the OTP sent to 'fab1@baf.com' previously to automate
        # the verification by 2FA
        otp = OTPManager().generate_otp()

        print(f"--> New generated OTP for automated test for {email} was: {otp}")

        set_otb_as_key = redis_set_key(
            redis_client=redis_client,
            key=email,
            value=otp)
        data = {"email": f"{email}", "verified_otp": f"{otp}"}

        async with AsyncClient(app=api, base_url="http://test") as ac:
            response = await ac.post(
                "/verify_otp",
                params=data)

        # email/otb means verification succeeded -> redict to /longin2fa
        assert response.status_code == 302


if __name__ == "__main__":
    unittest.main()
