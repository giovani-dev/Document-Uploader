

from datetime import datetime, timedelta
from email import message
from time import time
from uuid import UUID
from application.auth import decode_token, encode_token, is_inconsistent_token
from application.dto.error import Error
from application.dto.response import Response
from application.enum.status import StatusCode
from application.settings import Settings
from infra.database.models import User
from services.auth.dto.login import CredentialsDto
from passlib.hash import pbkdf2_sha256
from jose import jwt
from jose.constants import ALGORITHMS


async def make_credentials(user: User) -> Response[CredentialsDto]:
    token = await encode_token(
        claims={
            'type': 'token',
            'permissions': {
                'is_adm': user.is_adm,
                'is_external': user.is_external,
                'is_internal': user.is_internal
            },
            'user': str(user.external_id)
        },
        expire_limit=Settings.jwt_token_expire_limit
    )
    refresh_token = await encode_token(
        claims={
            'type': 'refresh',
            'user': str(user.external_id)
        },
        expire_limit=Settings.jwt_refresh_token_expire_limit
    )
    return Response(
        content=CredentialsDto(
            token=token,
            refresh_token=refresh_token
        ),
        status_code=StatusCode.Ok
    )


async def login(
    username: str,
    password: str
) -> Response[CredentialsDto | Error]:
    user = await User.find_one(User.email == username)
    is_pending = user.external_user.is_pending if user.external_user else None
    if not user or not pbkdf2_sha256.verify(password, user.password) or is_pending:
        return Response(
            content=Error(
                loc=['body'],
                message='Unauthorized user'
            ),
            status_code=StatusCode.Unauthorized
        )
    return await make_credentials(user)


async def refresh_token(data: CredentialsDto):
    token = await decode_token(token=data.token)
    _refresh_token = await decode_token(token=data.refresh_token)
    if await is_inconsistent_token(token, _refresh_token):
        return Response(
            content=Error(
                loc=['body'],
                message='Invalid token'
            ),
            message=StatusCode.Forbidden
        )
    now = time()
    if now >= token['exp'] or now >= _refresh_token['exp']:
        user = await User.find_one(User.external_id == UUID(_refresh_token['user']))
        return await make_credentials(user)
    return Response(
        content=CredentialsDto(
            token=data.token,
            refresh_token=data.refresh_token
        ),
        status_code=StatusCode.Ok
    )
