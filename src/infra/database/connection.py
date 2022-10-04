import motor
from typing import List
from beanie import init_beanie, Document
import urllib.parse


async def db_connect(
    password: str,
    user: str,
    host: str,
    models: List[Document]
):
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f'mongodb://{user}:{urllib.parse.quote(password)}@{host}/?authMechanism=DEFAULT'
    )
    await init_beanie(database=client.db_name, document_models=models)
