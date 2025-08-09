from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Создать мем 📌")]
    ],
    resize_keyboard=True
)

meme_templates_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Дрэйк 🦁", callback_data="drake"),
         InlineKeyboardButton(text="Бабулька 🦖", callback_data="grandma")],

        [InlineKeyboardButton(text="ВинниПух 🐻", callback_data="winbear")]
    ]
)

required_channels_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мастерская разработчика 👀", url="https://t.me/code_laba")]
    ]
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Кол-во пользователей 👨‍🦰"), KeyboardButton(text="Топ 10 💥")]
    ],
    resize_keyboard=True
)
