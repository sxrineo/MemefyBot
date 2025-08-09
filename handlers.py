from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile
from keyboards import main_menu_kb, meme_templates_kb, required_channels_kb, admin_kb
from fsm_states import MakeMemeFsm
from aiogram.fsm.context import FSMContext

from meme_maker import make_no_yes_meme
from private_config import bot, admins_ids
from db import add_user_into_db, get_users_count, get_top_x_meme_creators, increment_memes_count

router = Router()


def is_admin(user_id):
    if user_id in admins_ids:
        return True
    else:
        return False


@router.message(F.text == "/start")
async def handle_start(message: Message):
    await add_user_into_db(telegram_id=message.chat.id,
                           username=message.chat.username,
                           full_name=message.chat.full_name)
    await message.answer("Добро пожаловать! 😇", reply_markup=main_menu_kb)


@router.message(F.text == "/cancel", StateFilter("*"))
async def cancel_fsm(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Возвращаем в главное меню...", reply_markup=main_menu_kb)


@router.message(F.text == "Создать мем 📌")
async def handle_create_meme(message: Message, state: FSMContext):
    res = await bot.get_chat_member(user_id=message.chat.id, chat_id="-1002469271660")
    if res.status in ["member", "creator"]:
        await state.set_state(MakeMemeFsm.choosing_template)
        await message.answer("Выбери шаблон: 💡", reply_markup=meme_templates_kb)
    else:
        await state.clear()
        await message.answer("Ты не подписан на наши каналы: ⛔", reply_markup=required_channels_kb)


@router.callback_query()
async def handle_callback_query(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data in ["drake", "grandma", "winbear"]:
        await state.update_data(template=data)
        await state.set_state(MakeMemeFsm.entering_first_text)
        await callback_query.message.answer("Введи текст первого блока 📍")

    await callback_query.answer()


@router.message(MakeMemeFsm.entering_first_text)
async def catch_first_text(message: Message, state: FSMContext):

    await state.update_data(first_text=message.text)
    await message.answer("Введите текст второго блока 📍")
    await state.set_state(MakeMemeFsm.entering_second_text)


@router.message(MakeMemeFsm.entering_second_text)
async def catch_second_text(message: Message, state: FSMContext, bot: Bot):

    data = await state.get_data()
    first_text = data.get("first_text")
    second_text = message.text

    if data.get("template") == "drake":
        image_name = make_no_yes_meme(user_texts=[first_text, second_text], pos1=(130, 5), pos2=(130, 130),
                                      font_size=12, template_name="drake.jpg", max_line_length=120)
    elif data.get("template") == "grandma":
        image_name = make_no_yes_meme(user_texts=[first_text, second_text], pos1=(265, 5), pos2=(265, 220),
                                      font_size=18, template_name="grandma.jpg", max_line_length=220)
    elif data.get("template") == "winbear":
        image_name = make_no_yes_meme(user_texts=[first_text, second_text], pos1=(360, 5), pos2=(360, 295),
                                      font_size=24, template_name="winbear.jpg", max_line_length=450)
    else:
        return

    if image_name == "Текст слишком длиный для этого шаблона...":
        await message.answer("Текст слишком длиный для этого шаблона...\nВведи первый текст заново...")
        await state.set_state(MakeMemeFsm.entering_first_text)
    else:

        image_path = FSInputFile(f"user_memes/{image_name}")
        await bot.send_photo(chat_id=message.chat.id, photo=image_path)
        await state.clear()
        await increment_memes_count(message.chat.id)


@router.message(F.text == "/admin")
async def get_admin_kb(message: Message):
    if is_admin(user_id=message.chat.id):
        await message.answer("Админ панелька: 🦾", reply_markup=admin_kb)


@router.message(F.text == "Кол-во пользователей 👨‍🦰")
async def send_users_count(message: Message):
    if is_admin(user_id=message.chat.id):
        users_count = await get_users_count()
        await message.answer(f"Текущее число пользователей: {users_count}👨‍🦰")


@router.message(F.text == "Топ 10 💥")
async def send_top_stats(message: Message):
    if is_admin(user_id=message.chat.id):
        top = await get_top_x_meme_creators()
        res = ""
        for i, user in enumerate(top):
            res += f"TOP {i + 1}: {top[i][2]}, создано мемов: {top[i][5]}\n"
        await message.answer(res)
