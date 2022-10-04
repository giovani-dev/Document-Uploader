from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi import Response as ApiResponse
from application.api import callback
from application.auth import auth_claim_contains
from services.auth.domain.create_user import create_external_user, create_internal_user
from services.auth.domain.list_user import list_pendind_users
from services.auth.domain.update_user import aprove_external_user

from services.auth.dto.user import ApproveExternalUserDto, CreateExternalUserDto, CreateGenericUserDto
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(
    prefix='/user'
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/create/external')
async def api_create_external_user(
    body: CreateExternalUserDto,
    response: ApiResponse
):
    data = await create_external_user(body=body)
    return await callback(data, response)


@router.post('/create/internal')
@auth_claim_contains(is_adm=True)
async def api_create_internal_user(
    body: CreateGenericUserDto,
    response: ApiResponse,
    token: str = Depends(oauth2_scheme)
):
    data = await create_internal_user(body=body)
    return await callback(data, response)


@router.patch('/approve/external/{external_id}')
@auth_claim_contains(is_internal=True)
async def api_aprove_external_user(
    body: ApproveExternalUserDto,
    external_id: UUID,
    response: ApiResponse,
    token: str = Depends(oauth2_scheme)
):
    data = await aprove_external_user(
        external_id=external_id,
        is_pending=body.is_pending,
    )
    return await callback(data, response)


@router.get('/approve/external/list')
async def api_list_pending_users(
    response: ApiResponse,
    token: str = Depends(oauth2_scheme)
):
    data = await list_pendind_users()
    return await callback(data, response)
