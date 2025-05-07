import asyncio
import os
import re

from aiogram.filters import CommandObject, CommandStart, Command
from aiogram.types import CallbackQuery, Message, FSInputFile, ReplyKeyboardRemove
from aiogram import F, Dispatcher, Router
from aiogram.utils.chat_action import ChatActionSender
import app.keyboards as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


from app.questions import questions
from filters.is_admin import IsAdmin
from config import bot, admins
from config import all_media_dir





handlers_router = Router()


class Reg(StatesGroup):
    name = State()
    number = State()


class Form(StatesGroup): 
    name = State()
    age = State()




def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    else:
        return None

      
class Form(StatesGroup):
    gender = State()
    age = State()
    full_name = State()
    user_login = State()
    photo = State()
    about = State()
    check_state = State()


questionnaire_router = Router()


@questionnaire_router.message(Command('start_questionnaire'))
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Привет. Для начала выбери свой пол: ', reply_markup=kb.gender_kb())
    await state.set_state(Form.gender)


@questionnaire_router.message((F.text.lower().contains('мужчина')) | (F.text.lower().contains('женщина')), Form.gender)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(gender=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Супер! А теперь напиши сколько тебе полных лет: ', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.age)


@questionnaire_router.message(F.text, Form.gender)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Пожалуйста, выбери вариант из тех что в клавиатуре: ', reply_markup=kb.gender_kb())
    await state.set_state(Form.gender)


@questionnaire_router.message(F.text, Form.age)
async def start_questionnaire_process(message: Message, state: FSMContext):
    check_age = extract_number(message.text)

    if not check_age or not (1 <= int(message.text) <= 100):
        await message.reply("Пожалуйста, введите корректный возраст (число от 1 до 100).")
        return

    await state.update_data(age=check_age)
    await message.answer('Теперь укажите свое полное имя:')
    await state.set_state(Form.full_name)


@questionnaire_router.message(F.text, Form.full_name)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    text = 'Теперь укажите ваш логин, который будет использоваться в боте'

    if message.from_user.username:
        text += ' или нажмите на кнопку ниже и в этом случае вашим логином будет логин из вашего телеграмм: '
        await message.answer(text, reply_markup=kb.get_login_tg())
    else:
        text += ' : '
        await message.answer(text)

    await state.set_state(Form.user_login)

# вариант когда мы берем логин из профиля телеграмм
@questionnaire_router.callback_query(F.data, Form.user_login)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Беру логин с телеграмм профиля')
    await call.message.edit_reply_markup(reply_markup=None)
    await state.update_data(user_login=call.from_user.username)
    await call.message.answer('А теперь отправьте фото, которое будет использоваться в вашем профиле: ')
    await state.set_state(Form.photo)


# вариант когда мы берем логин из введенного пользователем
@questionnaire_router.message(F.text, Form.user_login)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(user_login=message.from_user.username)
    await message.answer('А теперь отправьте фото, которое будет использоваться в вашем профиле: ')
    await state.set_state(Form.photo)


@questionnaire_router.message(F.photo, Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await message.answer('А теперь расскажите пару слов о себе: ')
    await state.set_state(Form.about)


@questionnaire_router.message(F.document.mime_type.startswith('image/'), Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    photo_id = message.document.file_id
    await state.update_data(photo=photo_id)
    await message.answer('А теперь расскажите пару слов о себе: ')
    await state.set_state(Form.about)


@questionnaire_router.message(F.document, Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, отправьте фото!')
    await state.set_state(Form.photo)


@questionnaire_router.message(F.text, Form.about)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(about=message.text)

    data = await state.get_data()

    caption = f'Пожалуйста, проверьте все ли верно: \n\n' \
              f'<b>Полное имя</b>: {data.get("full_name")}\n' \
              f'<b>Пол</b>: {data.get("gender")}\n' \
              f'<b>Возраст</b>: {data.get("age")} лет\n' \
              f'<b>Логин в боте</b>: {data.get("user_login")}\n' \
              f'<b>О себе</b>: {data.get("about")}'

    await message.answer_photo(photo=data.get('photo'), caption=caption, reply_markup=kb.check_data())
    await state.set_state(Form.check_state)

# сохраняем данные
@questionnaire_router.callback_query(F.data == 'correct', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Данные сохранены')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Благодарю за регистрацию. Ваши данные успешно сохранены!')
    await state.clear()


# запускаем анкету сначала
@questionnaire_router.callback_query(F.data == 'incorrect', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Запускаем сценарий с начала')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Привет. Для начала выбери свой пол: ', reply_markup=kb.gender_kb())
    await state.set_state(Form.gender)






@handlers_router.message(Command(commands=['start_2']))
async def cmd_start(message: Message):
    await message.reply(f"Привет, {message.from_user.first_name}  ID: {message.from_user.id}",
                        reply_markup=kb.main)

@handlers_router.message(F.text.upper().contains('ПРИВ'))
async def cmd_start(message: Message):
    await message.reply(f"Привет, {message.from_user.first_name}  ID: {message.from_user.id}",
                        reply_markup=kb.main)


@handlers_router.message(Command(commands=['help', 'problem']))
async def get_help(message: Message):
    await message.answer('Чем могу помочь ?')

@handlers_router.message(F.text.upper().contains('КАК ДЕЛА?') )
async def how_are_you(message: Message):
    await message.answer('Блястяще')


# @handlers_router.message(F.photo)
# async def how_are_you(message: Message):
#     await message.answer(f' ID photo {message.photo[-1].file_id}')

# @handlers_router.message(Command('get_photo'))
# async def get_photo(message: Message):
#     await message.answer_photo(photo='AgACAgIAAxkBAAMIaAS80cMj54gNeW9gy9AMXbmtnX4AAoXrMRutnyhIr1a44I7dIy0BAAMCAAN5AAM2BA',
#                                caption='Image')
    
@handlers_router.message(F.text == 'Корзина')
async def how_are_you(message: Message):
    await message.answer('Вот корзинка')

@handlers_router.message(F.text == 'О нас')
async def how_are_you(message: Message):
    await message.reply("Мы есть на:", reply_markup=kb.ease_link_kb())


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


@handlers_router.message(F.text == 'Давай инлайн')
async def get_inline_link(message: Message):
    await message.answer('Вот инлайн', reply_markup=kb.get_inline_kb())

# @handlers_router.callback_query(F.data == 'back_home')
# async def get_inline_link(call: CallbackQuery):
#     # await call.answer()
#     await call.answer('Вот главная')
#     await call.message.answer(reply_markup=)


@handlers_router.callback_query(F.data == 'get_person')
async def send_random_person(call: CallbackQuery):
    await call.answer('Генерирую случайного пользователя')
    user = kb.get_random_person()
    formatted_message = (
        f"👤 <b>Имя:</b> {user['name']}\n"
        f"🏠 <b>Адрес:</b> {user['address']}\n"
        f"📧 <b>Email:</b> {user['email']}\n"
        f"📞 <b>Телефон:</b> {user['phone_number']}\n"
        f"🎂 <b>Дата рождения:</b> {user['birth_date']}\n"
        f"🏢 <b>Компания:</b> {user['company']}\n"
        f"💼 <b>Должность:</b> {user['job']}\n"
    )
    await call.message.answer(formatted_message)


@handlers_router.callback_query(F.data == 'back_home')
async def back_home(call: CallbackQuery):
    await call.message.answer(text='вот', reply_markup=kb.main, )
    await call.answer()


@handlers_router.message(Command('faq'))
async def cmd_start_2(message: Message):
    await message.answer('Сообщение с инлайн клавиатуры,', reply_markup=kb.create_qst_inline_kb(questions))


@handlers_router.callback_query(F.data.startswith("qst_"))
async def cmd_start(call: CallbackQuery):
    await call.answer()
    qst_id = int(call.data.replace('qst_', ''))
    qst_data = questions[qst_id]
    msg_text = f'Ответ на вопрос {qst_data.get("qst")}\n\n' \
               f'<b>{qst_data.get("answer")}</b>\n\n' \
               f'Выбери другой вопрос:'
    async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action="typing"):
        await asyncio.sleep(2)
        await call.message.answer(msg_text, reply_markup=kb.create_qst_inline_kb(questions))



@handlers_router.message(Command(commands=["settings", "about"]))
async def univers_cmd_handler(message: Message, command: CommandObject):
    command_args: str = command.args
    command_name = 'settings' if 'settings' in message.text else 'about'
    response = f'Была вызвана команда /{command_name}'
    if command_args:
        response += f' с меткой <b>{command_args}</b>'
    else:
        response += ' без метки'
    await message.answer(response)




@handlers_router.message(F.text.lower().contains('подписывайся'), IsAdmin(admins))
async def process_find_word(message: Message):
    await message.answer('О, админ, здарова! А тебе можно писать подписывайся.')


@handlers_router.message(F.text.lower().contains('подписывайся'))
async def process_find_word(message: Message):
    await message.answer('В твоем сообщении было найдено слово "подписывайся", а у нас такое писать запрещено!')


@handlers_router.message(F.text.lower().contains('тэги'))
async def process_find_word(message: Message):
    await message.answer(
                        "<b>Жирный</b>\n"
                        "<i>Курсив</i>\n"
                        "<u>Подчеркнутый</u>\n"
                        "<s>Зачеркнутый</s>\n"
                        "<tg-spoiler>Спойлер (скрытый текст)</tg-spoiler>\n"
                        "<a href='http://www.example.com/'>Ссылка в тексте</a>\n"
                        "<code>Код с копированием текста при клике</code>\n"
                        "<pre>Спойлер с копированием текста</pre>\n"
                        )



# @handlers_router.message(Command('send_audio'))
# async def cmd_start(message: Message, state: FSMContext):
#     audio_file = FSInputFile(path=os.path.join(all_media_dir, 'audio.mp3'), filename='1')
#     await message.answer_audio(audio=audio_file)


@handlers_router.message(Command('send_audio'))
async def cmd_start(message: Message, state: FSMContext):
    audio_file = FSInputFile(path=os.path.join(all_media_dir, 'audio.mp3'))
    msg_id = await message.answer_audio(audio=audio_file, reply_markup=kb.main_kb(message.from_user.id),
                                        caption='Моя <u>отформатированная</u> подпись к <b>файлу</b>')
    print(msg_id.audio.file_id)

    # 'CQACAgIAAxkDAAIBrWgUFvZyI7yjFwbF7u7goYyglU4xAAIPZQACoDChSMBTqKlDUqwtNgQ'


@handlers_router.message(Command('send_audio_2'))
async def cmd_start(message: Message, state: FSMContext):
    # audio_file = FSInputFile(path=os.path.join(all_media_dir, 'new_message_tone.mp3'))
    audio_id = 'CQACAgIAAxkDAAIBrWgUFvZyI7yjFwbF7u7goYyglU4xAAIPZQACoDChSMBTqKlDUqwtNgQ'
    msg_id = await message.answer_audio(audio=audio_id, reply_markup=kb.main_kb(message.from_user.id),
                                        caption='Моя <u>отформатированная</u> подпись к <b>файлу</b>')
    

@handlers_router.message(Command('send_photo'))
async def cmd_start(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join(all_media_dir, 'image.jpg'))
    msg_id = await message.answer_photo(photo=photo_file, reply_markup=kb.main_kb(message.from_user.id),
                                        caption='Моя <u>отформатированная</u> подпись к <b>фото</b>')
    print(msg_id.photo[-1].file_id)


@handlers_router.message(Command('link_photo'))
async def cmd_start(message: Message, state: FSMContext):
    photo_url = 'https://indirimlerce.com/wp-content/uploads/2023/02/phyton-ile-neler-yapilabilir.jpg'
    msg_id = await message.answer_photo(photo=photo_url, reply_markup=kb.main_kb(message.from_user.id),
                                        caption='Моя <u>отформатированная</u> подпись к <b>фото</b>')
    print(msg_id.photo[-1].file_id)


@handlers_router.message(Command('send_video'))
async def cmd_start(message: Message, state: FSMContext):
    video_file = FSInputFile(path=os.path.join(all_media_dir, 'video.mp4'))
    msg = await message.answer_video(video=video_file, reply_markup=kb.main_kb(message.from_user.id),
                                     caption='Моя отформатированная подпись к файлу')
    await asyncio.sleep(2)
    await message.answer_video(video=msg.video.file_id, caption='Новое описание к тому же видосу',
                               reply_markup=kb.main_kb(message.from_user.id))
    await msg.delete()


@handlers_router.message(Command('send_voice'))
async def cmd_start(message: Message, state: FSMContext):
    async with ChatActionSender.record_voice(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(3)
        await message.answer_voice(voice=FSInputFile(
            path=os.path.join(all_media_dir, 'audio.mp3')))