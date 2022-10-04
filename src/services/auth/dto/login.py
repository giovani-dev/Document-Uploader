from pydantic import BaseModel


class CredentialsDto(BaseModel):
    token: str
    refresh_token: str


class RefreshTokenDto(BaseModel):
    refresh_token: str
