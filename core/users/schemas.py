from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    email: str = Field(EmailStr)


class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class UserResponseSchema(BaseModel):
    id: int = Field(...)
    username: str = Field(...)
    email: str = Field(...)


class UserRefreshTokenSchema(BaseModel):
    token: str = Field(...)
