from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

async def client(token: str):
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    return bot


async def send_message_in_channel(token: str, chat_id_channel: int, message: dict, proxy: str = None):
    bot = await client(token)

    message = message.get("text")
    try:
        await bot.send_message(chat_id_channel, text = message)
    except Exception as e:
        print(e)
    finally:
        await bot.session.close()

