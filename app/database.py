import os
from asyncpg_lite import DatabaseManager
import asyncio

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

pg_link = os.getenv('DB_URL')



async def main():
    db_manager = DatabaseManager(dsn=pg_link)
    async with db_manager:
        pass

asyncio.run(main()) 