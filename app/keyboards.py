
from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    WebAppInfo,
    )
from faker import Faker
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import admins



main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог'), KeyboardButton(text='О нас')],
    [KeyboardButton(text='Корзина'), KeyboardButton(text='Контакты')],
    [KeyboardButton(text='Давай инлайн')]
    ], 
    resize_keyboard=True,
    input_field_placeholder='Выберете пункт меню', 
    one_time_keyboard=True)


def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="📖 О нас"), KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="📝 Заполнить анкету"), KeyboardButton(text="📚 Каталог")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

# settings = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Наш сайт', 
#                           url='https://novosibirsk.drom.ru/')]
#                           ])


def get_inline_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Генерировать пользователя", callback_data='get_person')],
        [InlineKeyboardButton(text="На главную", callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def ease_link_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Хабр", url='https://habr.com/ru/users/yakvenalex/')],
        [InlineKeyboardButton(text="Тelegram", url='tg://resolve?domain=yakvenalexx')],
        [InlineKeyboardButton(text="Мобильном приложении", web_app=WebAppInfo(url="https://tg-promo-bot.ru/questions"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def get_random_person():
    fake = Faker('ru_RU')

    user = {
        'name': fake.name(),
        'address': fake.address(),
        'email': fake.email(),
        'phone_number': fake.phone_number(),
        'birth_date': fake.date_of_birth(),
        'company': fake.company(),
        'job': fake.job()
    }
    return user



def create_qst_inline_kb(questions: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    # Добавляем кнопки вопросов
    for question_id, question_data in questions.items():
        builder.row(
            InlineKeyboardButton(
                text=question_data.get('qst'),
                callback_data=f'qst_{question_id}'
            )
        )
    # Добавляем кнопку "На главную"
    builder.row(
        InlineKeyboardButton(
            text='На главную',
            callback_data='back_home'
        )
    )
    # Настраиваем размер клавиатуры
    builder.adjust(1)
    return builder.as_markup()


