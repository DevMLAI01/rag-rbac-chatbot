from fastapi import APIRouter, HTTPException, status
from src.auth.models import LoginRequest, LoginResponse
from src.auth.user_store import authenticate
from src.auth.jwt_handler import create_token
from config.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(body: LoginRequest):
    user = authenticate(body.username, body.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_token(user.user_id, user.role)
    return LoginResponse(
        access_token=token,
        role=user.role,
        expires_in=settings.jwt_expire_hours * 3600,
    )
