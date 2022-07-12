from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # TODO
from fastapi.responses import JSONResponse # TODO remove to use HTTPException instead
from pydantic.error_wrappers import ValidationError

from auth.user import User
from auth.security import PasswordManager, OTPManager, JWTManager

from api.main import mongo_client, redis_client
from api.databases import (
        mongo_insert_one,
        mongo_find_one,
        redis_set_key,
        redis_get_key,
        redis_get_ttl)


router = APIRouter()

@router.post("/register")
def register(username: str, email: str, password: str,
        gender: str, cooker: bool, enable_2fa: bool):
    try:
        _username = mongo_find_one(
                mongo_client=mongo_client,
                collection="user",
                fields={"username": username},
                filter_options={"_id"})

        if _username:
            return JSONResponse(
                    status_code=409,
                    content={"message": f"username '{username}' is already in use"})

        _email = mongo_find_one(
                mongo_client=mongo_client,
                collection="user",
                fields={"email": email},
                filter_options={"_id"})

        if _email:
            return JSONResponse(
                    status_code=409,
                    content={"message": f"'{email}' is already in use"})

        _hashed_password = PasswordManager().compute_hash_password(password)
        user = User(
                username=username,
                email=email,
                hashed_password=_hashed_password,
                gender=gender,
                cooker=cooker,
                enabled_2fa=enable_2fa)

        _id = mongo_insert_one(
                mongo_client=mongo_client,
                collection="user",
                data=user.dict())

        if enable_2fa:
            otp = OTPManager().generate_otp()
            key_is_set = redis_set_key(redis_client=redis_client, key=email, value=otp)

            # TODO
            # if enable_2fa send an email (smtplib) with OTP or print OTP to stdout
            # if verification succeeded save user to the database

        return JSONResponse(
                status_code=201,
                content={"message": f"{username} you have been successfully registered"})
    except ValidationError as e:
        return JSONResponse(
                status_code=400,
                content={"message": f"{e}"})


@router.post("/login")
def login(email: str, password: str):
    try:
        user = mongo_find_one(
                mongo_client=mongo_client,
                collection="user",
                fields={"email": email},
                filter_options={"username", "hashed_password", "enabled_2fa"})

        if user:
            confirmed_password = PasswordManager().verify_password(password, user["hashed_password"])
            if not confirmed_password:
                return JSONResponse(status_code=400, content={"message": f"wrong combination of email and password"})
            if confirmed_password and user["enabled_2fa"]:
                # TODO redirect /login2fa
                return {"message": "TODO redirect /login2fa"}
            return JSONResponse(status_code=200, content={"message": f"{user['username']} you have been successfully logged in"})
        return JSONResponse(status_code=400, content={"message": f"wrong combination of email and password"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"{e}"})


@router.post("/login2fa")
def login2fa(email: str, password: str):
    user = mongo_find_one(
            mongo_client=mongo_client,
            collection="user",
            fields={"email": email},
            filter_options={"username", "hashed_password", "enabled_2fa"})

    if not user:
        return JSONResponse(status_code=400, content={"message": f"wrong combination of email and password"})

    confirmed_password = PasswordManager().verify_password(password, user["hashed_password"])
    if not confirmed_password:
        return JSONResponse(status_code=400, content={"message": f"wrong combination of email and password"})

    if confirmed_password and user["enabled_2fa"]:
        otp = redis_get_key(redis_client=redis_client, key=email)

        if not otp:
            # means OTP has expired from Redis cache
            # generate a new one
            otp = OTPManager().generate_otp()
            key_is_set = redis_set_key(
                    redis_client=redis_client,
                    key=email,
                    value=otp)

            # TODO
            # implement JWT with OAuth2, verify and proceed
        return JSONResponse(
                status_code=200,
                content={"message": f"You have been succesfully loged"})
    # TODO redirect to /login
    return {"message": "TODO redirect /login"}
