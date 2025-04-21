from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог'), KeyboardButton(text='О нас')],
    [KeyboardButton(text='Корзина'), KeyboardButton(text='Контакты')],
    ], 
    resize_keyboard=True,
    input_field_placeholder='Выберете пункт меню')

main_01 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
    [InlineKeyboardButton(text='Корзина', callback_data='basket')],
    [InlineKeyboardButton(text='Контакты', callback_data='contacts')],
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Наш сайт', 
                          url='https://novosibirsk.drom.ru/')]
                          ])