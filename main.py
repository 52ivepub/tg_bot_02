import asyncio
import os
import logging
from aiogram import Bot, Dispatcher

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import F
from app.handlers import handlers_router
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
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)
    await set_commands()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except Exception:
        print('Bot sleep')