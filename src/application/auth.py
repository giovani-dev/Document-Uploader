from datetime import datetime, timedelta
from functools import wraps
from typing import List
import copy

from fastapi import HTTPException
from application.api import callback
from application.dto.error import Error
from application.dto.response import Response
from application.enum.status import StatusCode
from application.settings import Settings
from jose import JWTError, jwt
from jose.constants import ALGORITHMS


async def is_inconsistent_token(token: dict, refresh_token: dict):
    return token['user'] != refresh_token['user'] or \
        token['type'] != 'token' or \
            refresh_token['type'] != 'refresh'


async def decode_token(token):
    return jwt.decode(
        token,
        Settings.jwt_token_secret,
        algorithms=ALGORITHMS.HS512
    )


async def encode_token(claims: dict, expire_limit: datetime):
    claims.update({
        'exp': datetime.timestamp(
            datetime.now() + timedelta(seconds=expire_limit)
        ),
    })
    return jwt.encode(
        claims=claims,
        key=Settings.jwt_token_secret,
        algorithm=ALGORITHMS.HS512
    )


async def verify_token(token: str, claims: List[str]) -> bool:
    try:
        decoded_token = await decode_token(token)
    except JWTError:
        return False
    if decoded_token['type'] != 'token':
        return False
    is_valid = False
    for claim in claims:
        if decoded_token['permissions'][claim]:
            is_valid = True
        else:
            is_valid = False
    return is_valid




def auth_claim_contains(**claims):
    def auth(func):
        _claims = copy.deepcopy(claims)
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not await verify_token(kwargs.get('token'), _claims):
                return await callback(
                    Response(
                        content=Error(
                            loc=['header', 'Authorization'],
                            message="Unauthorized user"
                        ),
                        status_code=StatusCode.Forbidden
                    ),
                    kwargs.get('response')
                )
            return await func(*args, **kwargs)
        return wrapper
    return auth