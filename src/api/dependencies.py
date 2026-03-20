from fastapi import Request, Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.jwt_handler import decode_token
from src.auth.models import TokenPayload

_bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(_bearer),
) -> TokenPayload:
    return decode_token(credentials.credentials)


async def get_raw_token(
    credentials: HTTPAuthorizationCredentials = Security(_bearer),
) -> str:
    return credentials.credentials


async def get_graph(request: Request):
    return request.app.state.graph
