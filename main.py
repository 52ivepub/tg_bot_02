import asyncio
import os
import logging
from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv
from aiogram.types import Message
from aiogram import F
from app.handlers import handlers_router

load_dotenv(find_dotenv())


bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

dp.include_routers(handlers_router)

async def on_shutdown(bot):
    print("=========БОТ УСНУЛ=========")

async def main():
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except Exception:
        print('Bot sleep')