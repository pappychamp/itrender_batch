import os
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
HOST_NAME = os.environ.get("HOST_NAME")
PORT_NUMBER = os.environ.get("PORT_NUMBER")

DB_URL = "{}://{}:{}@{}:{}/{}".format(
    "postgresql+asyncpg",
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    HOST_NAME,
    PORT_NUMBER,
    POSTGRES_DB,
)
Engine = create_async_engine(DB_URL, echo=False)
Session = async_scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=Engine,
        class_=AsyncSession,
        expire_on_commit=False,
    ),
    scopefunc=current_task,
)
Base = declarative_base()

# if __name__ == "__main__":
#     import asyncio

#     async def async_main():
#         async with Engine.begin() as conn:
#             await conn.run_sync(Base.metadata.create_all)

#     asyncio.run(async_main())
