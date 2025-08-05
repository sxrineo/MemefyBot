import asyncio

import aiosqlite


async def db_init():
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            memes_count INTEGER DEFAULT 0
            );
        """)
        await db.commit()


async def add_user_into_db(telegram_id: int, username: str, full_name: str):
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("INSERT OR IGNORE INTO users (telegram_id, username, full_name) VALUES (?, ?, ?)",
                         (telegram_id,
                          username,
                          full_name))
        await db.commit()


async def get_users_count():
    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            row = await cursor.fetchone()
            return row[0]


async def get_top_x_meme_creators(x: int = 10):
    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT * FROM users ORDER BY memes_count DESC") as cursor:
            row = await cursor.fetchmany(x)
            return row


async def increment_memes_count(telegram_id):
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("""
            UPDATE users
            SET memes_count = memes_count + 1
            WHERE telegram_id = ?
        """, (telegram_id,))
        await db.commit()


asyncio.run(get_top_x_meme_creators(x=5))

