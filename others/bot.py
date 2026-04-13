#Мой папа думает что я проститутка

import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


def client(token: str):
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    return bot


async def send_message_in_channel(token: str, chat_id_channel: int, message: dict, proxy: str = None):
    bot = client(token)

    text = message.get("text")
    try:
        await bot.send_message(chat_id=chat_id_channel, text=text, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(e)
        raise RuntimeError(f'ERROR {str(e)}')
    finally:
        await bot.session.close()


async def bot_info(token: str):
    bot = client(token)
    try:
        info = await bot.get_me()
        return info
    except Exception as e:
        raise RuntimeError(f"Ошибка при получении информации о боте {str(e)}")
    finally:
        await bot.session.close()
