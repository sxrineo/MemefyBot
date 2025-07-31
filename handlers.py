from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import main_menu_kb, meme_templates_kb
from fsm_states import MakeMemeFsm
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(F.text == "/start")
async def handle_start(message: Message):
    await message.answer("Добро пожаловать!", reply_markup=main_menu_kb)


@router.message(F.text == "Создать мем")
async def handle_create_meme(message: Message, state: FSMContext):
    await state.set_state(MakeMemeFsm.choosing_template)
    await message.answer("Выбери шаблон", reply_markup=meme_templates_kb)


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



