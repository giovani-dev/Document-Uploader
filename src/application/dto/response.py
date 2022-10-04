


from typing import Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

from application.enum.status import StatusCode


TContent = TypeVar('TContent')


class Response(GenericModel, Generic[TContent]):
    content: TContent
    status_code: StatusCode
