from enum import Enum


class StatusCode(Enum):
    Ok = 200
    Created = 201
    NoContent = 204
    Unauthorized = 401
    BadRequest = 400
    Forbidden = 403
    InternalServerError = 500
