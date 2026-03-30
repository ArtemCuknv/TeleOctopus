import sqlite3 as s
from pathlib import Path

import others.bot as bot_module

DB_FILE = Path(__file__).resolve().parent.parent / 'database.db'

async def create_db():
    with s.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS bots(
                  id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  token TEXT, 
                  bot_name TEXT
                  )''')
        conn.commit()

async def add_bot(token):
    try:

        info = await bot_module.bot_info(token)
        bot_name = getattr(info, 'first_name', None) or getattr(info, 'username', None)

        if not bot_name:
            raise ValueError(f"Не удалось получить имя бота из bot_info для токена: {token}")

        with s.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO bots (token, bot_name) VALUES (?, ?)", (token, bot_name))
            conn.commit()
    except Exception as e:
        raise "Непредвиденная ошибка при добавлении бота: " + str(e)