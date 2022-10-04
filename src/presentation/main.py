import os
import sys


path = f'./{os.path.dirname(os.path.dirname(__file__))}'
sys.path.append(path)


import asyncio
import uvicorn
import fire

from application.settings import Settings
from infra.database.connection import db_connect
from infra.database.models import User
from services.auth.domain.create_user import create_adm


async def execute_create_adm(password, email, name):
    await db_connect(
        password=Settings.mongo_password,
        user=Settings.mongo_user,
        host=Settings.mongo_host,
        models=[User]
    )
    await create_adm(
        password=password,
        email=email,
        name=name
    )


def api():
    uvicorn.run(
        'presentation.api:app',
        port=Settings.auth_api_port,
        log_level='info'
    )


def adm(operation, password = None, email = None, name = None):
    match operation:
        case 'create':
            if password and email and name:
                asyncio.run(execute_create_adm(password, email, name))
            else:
                raise ValueError('You need to pass an username and password as parameter')
        case default:
            raise ValueError('Incorrect operation')



if __name__ == '__main__':
    fire.Fire({
        'adm': adm,
        'api': api
    })