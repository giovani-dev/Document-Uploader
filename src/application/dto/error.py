from typing import List
from pydantic import BaseModel


class Error(BaseModel):
    loc: List[str]
    message: str
