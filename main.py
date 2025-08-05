import asyncio
from private_config import dp, bot
from handlers import router

dp.include_router(router=router)


async def start_bot():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())

