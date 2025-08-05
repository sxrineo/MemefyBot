from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Создать мем")]
    ],
    resize_keyboard=True
)

meme_templates_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Стандарт X", callback_data="Standart_X_template")]
    ]
)

required_channels_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мастерская разработчика", url="https://t.me/code_laba")]
    ]
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Кол-во пользователей"), KeyboardButton(text="Топ X")]
    ],
    resize_keyboard=True
)
