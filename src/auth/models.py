from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenPayload(BaseModel):
    sub: str        # user_id
    role: str
    exp: int


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    expires_in: int


class UserRecord(BaseModel):
    user_id: str
    username: str
    hashed_password: str
    role: str
    display_name: str
