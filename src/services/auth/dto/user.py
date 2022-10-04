

from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel


class CreateGenericUserDto(BaseModel):
    email: str
    name: str
    password: str


class CallbackGenericUserDto(BaseModel):
    external_id: UUID
    email: str
    name: str


class CreateExternalUserDto(BaseModel):
    email: str
    name: str
    password: str
    gender: str
    birthday: date


class CallbackExternalUserDto(BaseModel):
    external_id: UUID
    email: str
    name: str
    gender: str
    birthday: date


class UpdateUserDto(BaseModel):
    name: str | None
    gender: str | None
    birthday: date | None


class ApproveExternalUserDto(BaseModel):
    is_pending: bool
