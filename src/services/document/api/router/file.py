import mimetypes
from fastapi import APIRouter, Depends, File, Response, UploadFile
from fastapi import Response as ApiResponse
from fastapi.security import OAuth2PasswordBearer
from application.auth import auth_claim_contains
from services.document.domain.file import download_from_s3, upload_to_s3
from application.api import callback
from fastapi.responses import StreamingResponse


router = APIRouter(
    prefix='/file'
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/upload')
@auth_claim_contains(is_external=True)
async def api_upload_document(
    response: ApiResponse,
    token: str = Depends(oauth2_scheme),
    file: UploadFile = File(...)
):
    data = await upload_to_s3(
        file_name=file.filename,
        content=file.file.read(),
        token=token
    )
    return await callback(data, response)


@router.get('/download')
@auth_claim_contains(is_external=True)
async def api_upload_document(
    file_name: str,
    response: ApiResponse,
    token: str = Depends(oauth2_scheme)
):
    data, filename = await download_from_s3(
        file_name=file_name,
    )
    return Response(data, media_type=mimetypes.MimeTypes().guess_type(filename)[0])

