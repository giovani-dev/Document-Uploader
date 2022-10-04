# from application.settings import Settings
from application.settings import Settings
from infra.database.connection import db_connect
from infra.database.models import DocumentReference, User
from fastapi import FastAPI
from services.auth.api.router import user, auth
from services.document.api.router import file


app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(file.router)


@app.on_event('startup')
async def startup_event():
    await db_connect(
        password=Settings.mongo_password,
        user=Settings.mongo_user,
        host=Settings.mongo_host,
        models=[User, DocumentReference]
    )


@app.on_event("shutdown")
async def shutdown_event():
    pass