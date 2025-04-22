from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, Message
from aiogram import F, Dispatcher, Router
import app.keyboards as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


handlers_router = Router()


class Reg(StatesGroup):
    name = State()
    number = State()



@handlers_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f"Hello, your ID: {message.from_user.id},\nfirst_name: {message.from_user.first_name}",
                        reply_markup=kb.main_01)


@handlers_router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Чем могу помочь ?')

@handlers_router.message(F.text == 'как дела?')
async def how_are_you(message: Message):
    await message.answer('Блястяще')


@handlers_router.message(F.photo)
async def how_are_you(message: Message):
    await message.answer(f' ID photo {message.photo[-1].file_id}')

@handlers_router.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMIaAS80cMj54gNeW9gy9AMXbmtnX4AAoXrMRutnyhIr1a44I7dIy0BAAMCAAN5AAM2BA',
                               caption='Image')
    
@handlers_router.message(F.text == 'Корзина')
async def how_are_you(message: Message):
    await message.answer('Вот корзинка')


@handlers_router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Вы запросили каталог')


@handlers_router.message(Command('reg'))
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите ваше имя')


@handlers_router.message(Reg.name)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите номер телефона')

@handlers_router.message(Reg.number)
async def two_three(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f'Спасибо, регистрация завершена\nName: {data["name"]}\nNumber: {data["number"]}')
    await state.clear()




