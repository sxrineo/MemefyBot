from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from keyboards import main_menu_kb, meme_templates_kb, required_channels_kb, admin_kb
from fsm_states import MakeMemeFsm
from aiogram.fsm.context import FSMContext
from private_config import bot, admins_ids
from db import add_user_into_db, get_users_count, get_top_x_meme_creators

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
    await message.answer("Добро пожаловать!", reply_markup=main_menu_kb)


@router.message(F.text == "/cancel", StateFilter("*"))
async def cancel_fsm(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Возвращаем в главное меню...", reply_markup=main_menu_kb)


@router.message(F.text == "Создать мем")
async def handle_create_meme(message: Message, state: FSMContext):
    res = await bot.get_chat_member(user_id=message.chat.id, chat_id="-1002469271660")
    if res.status in ["member", "creator"]:
        await state.set_state(MakeMemeFsm.choosing_template)
        await message.answer("Выбери шаблон", reply_markup=meme_templates_kb)
    else:
        await state.clear()
        await message.answer("Ты не подписан на наши каналы:", reply_markup=required_channels_kb)


@router.callback_query()
async def handle_callback_query(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == "Standart_X_template":
        await state.update_data(template=data)
        await state.set_state(MakeMemeFsm.entering_text)
        await callback_query.message.answer("Введи текст для мема")
    await callback_query.answer()


@router.message(MakeMemeFsm.entering_text)
async def catch_user_meme_text(message: Message, state: FSMContext):

    data = await state.get_data()

    await message.answer(f"template: {data.get('template')}, result: {message.text}")
    await state.clear()


@router.message(F.text == "/admin")
async def get_admin_kb(message: Message):
    if is_admin(user_id=message.chat.id):
        await message.answer("Админ панелька:", reply_markup=admin_kb)


@router.message(F.text == "Кол-во пользователей")
async def send_users_count(message: Message):
    if is_admin(user_id=message.chat.id):
        users_count = await get_users_count()
        await message.answer(f"Текущее число пользователей: {users_count}")


@router.message(F.text == "Топ X")
async def send_top_stats(message: Message):
    if is_admin(user_id=message.chat.id):
        top = await get_top_x_meme_creators()
        res = ""
        for i, user in enumerate(top):
            res += f"TOP {i + 1}: {top[i][2]}, memes count: {top[i][5]}\n"
        await message.answer(res)
