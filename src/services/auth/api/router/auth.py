from fastapi import APIRouter, Depends
from fastapi import Response as ApiResponse
from fastapi.security import HTTPBasicCredentials
from application.api import callback
from application.auth import auth_claim_contains

from services.auth.domain.auth import login, refresh_token
from services.auth.dto.login import CredentialsDto, RefreshTokenDto
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(
    prefix='/auth'
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/login')
async def api_login(body: HTTPBasicCredentials, response: ApiResponse):
    data = await login(username=body.username, password=body.password)
    return await callback(data, response)


@router.post('/refresh')
async def api_refresh_token(
    body: RefreshTokenDto,
    response: ApiResponse,
    token: str = Depends(oauth2_scheme)
):
    data = await refresh_token(data=CredentialsDto(
        token=token,
        refresh_token=body.refresh_token
    ))
    return await callback(data, response)
