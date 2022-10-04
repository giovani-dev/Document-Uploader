from typing import List
from application.dto.response import Response
from application.enum.status import StatusCode
from infra.database.models import User
from services.auth.dto.user import CallbackExternalUserDto
from application.dto.error import Error


async def list_pendind_users() -> Response[List[CallbackExternalUserDto] | Error]:
    users = await User.find_many(User.external_user.is_pending == True).to_list()
    user_list = [CallbackExternalUserDto(
        external_id=user.external_id,
        email=user.email,
        name=user.name,
        gender=user.external_user.gender,
        birthday=user.external_user.birthday
    ) for user in users]
    if len(user_list) == 0:
        status = StatusCode.NoContent
    else:
        status = StatusCode.Ok
    return Response(
        content=user_list,
        status_code=status
    )
