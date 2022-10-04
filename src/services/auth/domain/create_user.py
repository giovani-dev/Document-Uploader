import asyncio
from datetime import datetime
from email import message
from uuid import UUID, uuid4
from passlib.hash import pbkdf2_sha256
from application.dto.error import Error
from application.dto.response import Response
from application.enum.status import StatusCode
from pymongo.errors import DuplicateKeyError
from infra.database.models import User
from services.auth.dto.user import CallbackExternalUserDto, CallbackGenericUserDto, CreateExternalUserDto, CreateGenericUserDto


async def _create_user(
    data: dict,
    to_execute_in_success_callback,
    is_adm: bool = False,
    is_internal: bool = False,
    is_external: bool = False
) -> Response[CallbackGenericUserDto | CreateGenericUserDto | Error]:
    try:
        data['password'] = pbkdf2_sha256.hash(data['password'])
        to_insert = User(
            **data,
            external_id=uuid4(),
            is_adm=is_adm,
            is_internal=is_internal,
            is_external=is_external,
        )
        await to_insert.insert()
    except DuplicateKeyError as err:
        return Response[Error](
            content=Error(
                loc=['body.email', data['email']],
                message='E-mail already in use'
            ),
            status_code=StatusCode.BadRequest
        )
    except Exception as err:
        return Response[Error](
            content=Error(
                loc=['server'],
                message='Internal Server error'
            ),
            status_code=StatusCode.InternalServerError
        )
    return to_execute_in_success_callback(to_insert)


async def create_adm(email, name, password) -> Response[CallbackGenericUserDto | Error]:
    return await _create_user(
        data={
            'email': email,
            'name': name,
            'password': password
        },
        is_adm=True,
        to_execute_in_success_callback=lambda data: Response(
            content=CallbackGenericUserDto(
                external_id=data.external_id,
                email=data.email,
                name=data.name
            ),
            status_code=StatusCode.Created
        )
    )


async def create_internal_user(
    body: CreateGenericUserDto
) -> Response[CallbackGenericUserDto | Error]:
    return await _create_user(
        data=body.dict(),
        is_internal=True,
        to_execute_in_success_callback=lambda data: Response(
            content=CallbackGenericUserDto(
                external_id=data.external_id,
                email=data.email,
                name=data.name
            ),
            status_code=StatusCode.Created
        )
    )


async def create_external_user(
    body: CreateExternalUserDto
) -> Response[CallbackExternalUserDto | Error]:
    body = body.dict()
    user_data = {
        'external_user': {
            "gender": body.pop('gender'),
            "birthday": datetime.combine(body.pop('birthday'), datetime.min.time()),
            "is_pending": True
        }
    }
    body.update(user_data)
    return await _create_user(
        data=body,
        is_external=True,
        to_execute_in_success_callback=lambda data: Response(
            content=CallbackExternalUserDto(
                external_id=data.external_id,
                email=data.email,
                name=data.name,
                gender=data.external_user.gender,
                birthday=data.external_user.birthday
            ),
            status_code=StatusCode.Created
        )
    )
