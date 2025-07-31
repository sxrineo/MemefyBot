import asyncio
from aiogram import Bot, Dispatcher
from private_config import BOT_TOKEN
from handlers import router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router=router)


async def start_bot():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())

