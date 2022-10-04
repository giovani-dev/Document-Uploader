from uuid import UUID
from application.dto.error import Error
from application.dto.response import Response
from application.enum.status import StatusCode
from services.auth.dto.user import ApproveExternalUserDto, CallbackExternalUserDto, UpdateUserDto
from infra.database.models import User
from passlib.hash import pbkdf2_sha256


async def aprove_external_user(
    external_id: UUID,
    is_pending: bool = None
) -> Response[CallbackExternalUserDto | Error]:
    user = await User.find_one(User.external_id == external_id)
    if not user:
        return Response(
            content=Error(
                loc=['path', 'external_id'],
                message='User does not exist'
            ),
            status_code=StatusCode.BadRequest
        )
    if user.is_external and user.external_user.is_pending:
        user.external_user.is_pending = is_pending
        await user.save()
    else:
        return Response(
            content=Error(
                loc=['body', 'is_pending'],
                message='This external user is already approved'
            ),
            status_code=StatusCode.BadRequest
        )
    return Response(
        content=ApproveExternalUserDto(
            is_pending=user.external_user.is_pending
        ),
        status_code=StatusCode.Ok
    )