from uuid import UUID
from application.auth import decode_token
from application.dto.error import Error
from application.dto.response import Response
from application.enum.status import StatusCode
from application.settings import Settings
import boto3
import io
from infra.database.models import DocumentReference, User
from services.document.dto.document import DocumentReferenceDto
from sys import getsizeof
from jose.exceptions import ExpiredSignatureError
from botocore.exceptions import ClientError


if Settings.env == 'local':
    s3 = boto3.resource(
        service_name='s3',
        region_name=Settings.aws_region_name,
        aws_access_key_id=Settings.aws_access_key,
        aws_secret_access_key=Settings.aws_secret_key,
        endpoint_url="http://localhost:4566"
    )
else:
    s3 = boto3.resource(
        service_name='s3',
        region_name=Settings.aws_region_name,
        aws_access_key_id=Settings.aws_access_key,
        aws_secret_access_key=Settings.aws_secret_key
    )


def is_invalid_size(file_extension, content_size):
    _exe = file_extension == 'exe' and content_size <= 10
    _zip = file_extension == 'zip' and content_size <= 25
    _csv = file_extension == 'csv' and content_size <= 2
    _png = file_extension == 'png' and content_size <= 1
    _txt = file_extension == 'txt' and content_size <= 5
    _xlsx = file_extension == 'xlsx' and content_size <= 5
    return not (
        _exe or
        _zip or
        _csv or
        _png or
        _txt or
        _xlsx
    )


async def upload_to_s3(
    file_name: str,
    content: bytes,
    token: str
):
    content_size = getsizeof(content)/1048576
    file_extension = file_name.split('.')[-1]
    if not file_extension in ['txt', 'exe', 'zip', 'csv', 'xlsx', 'png']:
        return Response(
            content=Error(
                loc=['form-data', 'file'],
                message='File extension not suported'
            ),
            status_code=StatusCode.BadRequest
        )
    if is_invalid_size(file_extension, content_size):
        return Response(
            content=Error(
                loc=['form-data', 'file'],
                message='Max size has been exceeded'
            )
        )
    try:
        token = await decode_token(token)
    except ExpiredSignatureError:
        return Response(
            content=Error(
                loc=['header', 'Authorization'],
                message='Unauthorized user'
            ),
            status_code=StatusCode.Unauthorized
        )
    path = f"{token['user']}/{file_name}"
    # aws --endpoint-url=http://localhost:4566 s3 mb s3://teste-giovani
    bucket = s3.Bucket(Settings.aws_s3_bucket)
    bucket.upload_fileobj(
        io.BytesIO(content),
        path
    )
    document = DocumentReference(
        user_id=token['user'],
        document_path=path,
        filename=file_name,
        bucket_dir=f"{token['user']}/",
        bucket_name=Settings.aws_s3_bucket
    )
    try:
        await document.insert()
    except Exception:
        pass
    return Response(
        content=DocumentReferenceDto(
            **document.dict()
        ),
        status_code=StatusCode.Created
    )


async def download_from_s3(file_name: str, token: str = None):
    try:
        token = await decode_token(token)
    except ExpiredSignatureError:
        return Response(
            content=Error(
                loc=['header', 'Authorization'],
                message='Unauthorized user'
            ),
            status_code=StatusCode.Unauthorized
        )
    file = await DocumentReference.find_one(
        DocumentReference.document_path == file_name,
        DocumentReference.user_id == UUID(token['user'])
    )
    buffer = io.BytesIO()
    bucket = s3.Bucket(Settings.aws_s3_bucket)
    bucket.download_fileobj(file.document_path, buffer)
    return buffer.getvalue(), file.filename
