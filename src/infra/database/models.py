from datetime import datetime
from typing import List
from uuid import UUID
from beanie import Document, Indexed
from pydantic import BaseModel
from pydantic.generics import GenericModel


class GenericUser(GenericModel):
    email: Indexed(str, unique=True)
    name: str
    password: str


class ExternalUser(BaseModel):
    gender: str
    birthday: datetime
    is_pending: bool = True


class User(GenericUser, Document):
    external_id: Indexed(UUID, unique=True)
    is_adm: bool = False
    is_internal: bool = False
    is_external: bool = False
    external_user: ExternalUser | None = None


class DocumentReference(Document):
    user_id: UUID
    filename: str
    bucket_dir: str
    bucket_name: str
    document_path: Indexed(str, unique=True)