from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic.error_wrappers import ValidationError

from api.user import User

from api.security.password_manager import PasswordManager
from api.security.otp_manager import OTPManager
from api.security.jwt_manager import JWTManager

from api.main import mongo_client, redis_client
from api.databases.mongo import (
    mongo_insert_one,
    mongo_find_one,
    mongo_find_one_update
)

from api.databases.redis import (
    redis_set_key,
    redis_get_key,
    redis_delete_key
)

from api.config import BaseConfig


router = APIRouter()


@router.post("/register")
async def register(request: Request, username: str, email: str, password: str,
        gender: str, cooker: bool, enable_2fa: bool):
    """
    Register an user

    When registered and has not enable_2fa with an access token and redirects
    to /login
    """
    try:
        _username = mongo_find_one(
            mongo_client=mongo_client,
            collection="user",
            fields={"username": username},
            filter_option={"_id"})

        if _username:
            return HTTPException(
                status_code=409,
                detail={f"username '{username}' is already in use"})

        _email = mongo_find_one(
            mongo_client=mongo_client,
            collection="user",
            fields={"email": email},
            filter_option={"_id"})

        if _email:
            return HTTPException(
                status_code=409,
                detail={f"'{email}' is already in use"})

        hashed_password = PasswordManager().\
                compute_hash_password(password)

        if enable_2fa:
            otp = OTPManager().generate_otp()

            set_otb_as_key = redis_set_key(
                redis_client=redis_client,
                key=email,
                value=otp)

            print(f"OTP verification code for {email} is: {otp}")

            user = User(
                username=username,
                email=email,
                hashed_password=hashed_password,
                gender=gender,
                cooker=cooker,
                enabled_2fa=enable_2fa)

            _id = mongo_insert_one(
                mongo_client=mongo_client,
                collection="user",
                data=user.dict())

            return JSONResponse(
                status_code=201,
                content={"message": f"we sent you a verification code to '{email}'"})

        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            gender=gender,
            cooker=cooker,
            enabled_2fa=enable_2fa)

        _id = mongo_insert_one(
            mongo_client=mongo_client,
            collection="user",
            data=user.dict())

        if _id:
            # ObjectId is not used here, just to confirm the user creation
            request.session["skip_loggin"] = True
            request.session["email"] = email

            # set a JWT token
            access_token = JWTManager.generate_token(
                key="sub",
                value=email,
                secret_key=BaseConfig.JWT_SECRET_KEY)

            response = RedirectResponse(
                status_code=302,
                url=request.url_for("login"))

            response.set_cookie(
                "Authorization",
                value=f"Bearer {access_token}")

            return response
    except ValidationError as e:
        return HTTPException(
                status_code=400,
                detail={f"{e}"})


@router.get("/login")
def login(request: Request, email: str = None, password: str = None):
    """
    Handles user authentication with no 2FA enabled.
    """
    can_skip_loggin = request.session.get("skip_loggin")

    if can_skip_loggin:
        return JSONResponse(
            status_code=200,
            content={"message": "you logged in successfully after registration"})

    user = mongo_find_one(
        mongo_client=mongo_client,
        collection="user",
        fields={"email": email},
        filter_option={"username", "hashed_password", "enabled_2fa"})

    if not user:
        raise HTTPException(
            status_code=401,
            detail="incorrect email or password",
            headers={"WWW-Authenticate": "Basic"})

    confirmed_password = PasswordManager().\
        verify_password(
            password=password,
            hashed_password=user["hashed_password"])

    if not confirmed_password:
        raise HTTPException(
            status_code=401,
            detail="incorrect email or password",
            headers={"WWW-Authenticate": "Basic"})

    if user["enabled_2fa"]:
        # if a user enabled the 2FA, return 403
        raise HTTPException(
            status_code=403,
            detail="2FA is enabled, use /login2fa instead to verify",
            headers={"WWW-Authenticate": "Basic"})

    access_token = JWTManager.generate_token(
        key="sub",
        value=email,
        secret_key=BaseConfig.JWT_SECRET_KEY)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/login2fa")
def login2fa(request: Request, email: str = None, password: str = None):
    """
    Handles user authentication with 2FA enabled.

    If an OTP for a given email exist, we do not send a new OTP until it has
    been consumed (verified) by the user.

    OTP expires (lives in Redis) for 60 seconds.

    When an OTP has expired, we send a new one to the user's email when he tries
    to login again from this endpoint.

    When a user is finally verified, he logs in.
    """
    has_verified_otp = request.session.get("has_verified_otp")

    if has_verified_otp:
        return JSONResponse(
            status_code=200,
            content={"message": "you logged in successfully after verification"})

    user = mongo_find_one(
        mongo_client=mongo_client,
        collection="user",
        fields={"email": email},
        filter_option={"username", "hashed_password", "enabled_2fa", "verified_otp"})

    if not user:
        raise HTTPException(
            status_code=401,
            detail="incorrect email or password",
            headers={"WWW-Authenticate": "Basic"})

    confirmed_password = PasswordManager().\
        verify_password(
            password=password,
            hashed_password=user["hashed_password"])

    if not confirmed_password:
        raise HTTPException(
            status_code=401,
            detail="incorrect email or password",
            headers={"WWW-Authenticate": "Basic"})

    if not user["enabled_2fa"]:
        raise HTTPException(
            status_code=403,
            detail="2FA is not enabled, use /login instead",
            headers={"WWW-Authenticate": "Basic"})

    elif user["enabled_2fa"]:
        if not user["verified_otp"]:
            # avoid (spamming) the creation of new OTP for a given given email
            otp = redis_get_key(
                redis_client=redis_client,
                key=email)
            # if not OTP exist (expired) for an email, generate a new one
            if not otp:
                otp = OTPManager().generate_otp()

                print(f"new generated OTP '{otp}' for '{email}'")

                set_otb_as_key = redis_set_key(
                    redis_client=redis_client,
                    key=email,
                    value=otp)
                return {"message": f"we sent you a new verification code at '{email}'"}
            return {"message": f"please, confirm the code we sent you at '{email}'"}

    access_token = JWTManager.generate_token(
        key="sub",
        value=email,
        secret_key=BaseConfig.JWT_SECRET_KEY)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify_otp")
def verify_otp(request: Request, email:str, verified_otp: str):
    """
    If a match (email/OTP) is met, destroy the key from the cache -> consumed
    can not be used again.

    When no OTP has been set to an user's email, returns a 403
    """
    otp = redis_get_key(
        redis_client=redis_client,
        key=email)

    if otp:
        # match by email/OTP
        if otp.decode("utf-8") == verified_otp:
            user = mongo_find_one_update(
                mongo_client=mongo_client,
                collection="user",
                email=email,
                data={"verified_otp": True})

            # remove the email/otp pair from Redis cache
            verified_otp_removed = redis_delete_key(redis_client, email)

            if user and verified_otp_removed:
                request.session["has_verified_otp"] = True
                request.session["email"] = email

                response =  RedirectResponse(
                    status_code=302,
                    url=request.url_for("login2fa"))

                access_token = JWTManager.generate_token(
                    key="sub",
                    value=email,
                    secret_key=BaseConfig.JWT_SECRET_KEY)

                response.set_cookie(
                    "Authorization",
                    value=f"Bearer {access_token}")

                return response
    return JSONResponse(
        status_code=403,
        content={"message": "verification code has expired"})
