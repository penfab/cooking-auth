from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # TODO
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError

from auth.user import User
from auth.security import PasswordManager, OTPManager


router = APIRouter()

@router.post("/register")
def register(email: str, password: str, gender: str, cooker: bool, enable_2fa: bool):
    try:
        # TODO check if email not already in use

        pwdm = PasswordManager()
        hashed_password = pwdm.compute_hash_password(password)

        user = User(email=email,
                hashed_password=hashed_password,
                gender=gender,
                cooker=cooker,
                enabled_2fa=enable_2fa)

        # TODO save user to the database if not enable_2fa
        # if enable_2fa send an email with OTP or print OTP to stdout
        # if verification succeeded save user to the database

        data = user.dict() # TODO -> save to mongoDB

        if enable_2fa:
            otp = OTPManager().generate_otp() # TODO -> save to Redis with an expire time
            print(otp)

        return JSONResponse(status_code=200, content={"message": f"User {data} was registered succesfully"})
    except ValidationError as e:
        return JSONResponse(status_code=400, content={"message": f"{e}"})


@router.post("/login")
def login(email: str, password: str):
    try:
        # TODO check user from database, if enabled_2fa redirect to /login2fa
        # if not enabled_2fa check email/password
        return JSONResponse(status_code=200, content={"message": f"You have been logged succesfully"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"{e}"})


@router.post("/login2fa")
def login2fa(email):
    # TODO check user from database, check if enabled_2fa and OTP not expired
    # else generate new OTP, verify and proceed
    return JSONResponse(status_code=200, content={"message": f"You have been logged succesfully"})
