from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, ValidationError, validator


class Gender(str, Enum):
    FEMALE = "F"
    MALE = "M"


class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    gender: Gender
    cooker: bool
    enabled_2fa: bool
    joined_on: datetime = None

    class Config:
        use_enum_values = True


    @validator("username", pre=True, always=True)
    def set_username(cls, v):
        if len(v) < 3:
            raise ValueError("min. username length is 3")
        elif len(v) > 8:
            raise ValueError("max. username length is 8")
        return v.lower()

    @validator("gender", pre=True, always=True)
    def set_gender(cls, v):
        return v.upper()

    @validator("joined_on", always=True)
    def set_joined_on(cls, v):
        return datetime.now()
