#!/usr/bin/env python3
import aiosqlite
import asyncio

DB_PATH = 'users.db'

async def async_fetch_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users  # ✅ return result

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users  # ✅ return result

async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("[ALL USERS]")
    for user in all_users:
        print(user)

    print("[USERS AGE > 40]")
    for user in older_users:
        print(user)

# Run it
asyncio.run(fetch_concurrently())

