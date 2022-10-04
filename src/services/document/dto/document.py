


from uuid import UUID
from pydantic import BaseModel


class DocumentReferenceDto(BaseModel):
    user_id: UUID
    document_path: str
