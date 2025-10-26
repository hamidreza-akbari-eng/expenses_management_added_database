from auth.jwt_auth import (
    decode_refresh_token,
    generate_access_token,
    generate_refresh_token,
)
from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from users.models import UserModel
from users.schemas import (
    UserLoginSchema,
    UserRefreshTokenSchema,
    UserRegisterSchema,
    UserResponseSchema,
)

router = APIRouter(tags=["users"])


@router.post("/register", response_model=UserResponseSchema)
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    user_obj = UserModel(username=request.username, email=request.email)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found."
        )

    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    return user_obj


@router.post("/login", response_model=UserResponseSchema)
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=request.username).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found."
        )
    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication faled, incorrect password.",
        )
    access_token = generate_access_token(user_id=user_obj.id)
    refresh_token = generate_refresh_token(user_id=user_obj.id)
    response = JSONResponse(
        content={
            "detail": "Logged in successfully!",
            # "access_token": access_token,
            # "refresh_token": refresh_token,
        },
        status_code=status.HTTP_202_ACCEPTED,
    )

    access_max_age = 3600
    refresh_max_age = 24 * 3600
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=access_max_age,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=refresh_max_age,
        path="/",
    )
    return response


@router.post("/refresh-token")
async def user_refresh_token(request: UserRefreshTokenSchema):
    user_id = decode_refresh_token(request.token)
    access_token = generate_access_token(user_id)
    return JSONResponse(content={"access_token": access_token})
