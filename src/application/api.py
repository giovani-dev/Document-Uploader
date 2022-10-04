from fastapi import Depends, Response as ApiResponse
from fastapi.security import OAuth2PasswordBearer
from application.dto.response import Response as AppResponse


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def callback(data: AppResponse, response: ApiResponse):
    response.status_code = data.status_code.value
    return data.content
