import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import F
from sqlalchemy import BigInteger, Integer, String
from app.handlers import handlers_router
import os
from asyncpg_lite import DatabaseManager
import asyncio

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

pg_link = os.getenv('DB_URL')


# from  app.keyboards import set_commands

load_dotenv(find_dotenv())

admins = [int(admin_id) for admin_id in os.getenv('ADMINS').split(',')]

bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.include_routers(handlers_router)

async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='start_2', description='Старт 2'),
                BotCommand(command='faq', description='Частые вопросы')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def on_shutdown(bot):
    print("=========БОТ УСНУЛ=========")


async def main():
    await dp.start_polling(bot)
    await set_commands()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(main())
    except Exception as e:
        print('Bot sleep')
        print(e)