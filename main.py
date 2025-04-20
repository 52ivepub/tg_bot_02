import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from dotenv import find_dotenv, load_dotenv
from aiogram.types import Message
from aiogram import F

load_dotenv(find_dotenv())


bot = Bot(token=os.getenv("TOKEN"))

dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f"Hello, your ID: {message.from_user.id},\nfirst_name: {message.from_user.first_name}")


@dp.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Чем могу помочь ?')

@dp.message(F.text == 'как дела?')
async def how_are_you(message: Message):
    await message.answer('Блястяще')


@dp.message(F.photo)
async def how_are_you(message: Message):
    await message.answer(f' ID photo {message.photo[-1].file_id}')

@dp.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMIaAS80cMj54gNeW9gy9AMXbmtnX4AAoXrMRutnyhIr1a44I7dIy0BAAMCAAN5AAM2BA',
                               caption='Image')

async def main():
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except Exception:
        print('Bot sleep')