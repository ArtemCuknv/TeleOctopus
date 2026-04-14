from pyrogram import Client
from pyrogram.enums import ParseMode
from contextlib import asynccontextmanager


def create_client(
    api_id: int,
    api_hash: str,
    bot_token: str,
    proxy: dict | None = None,
    session_name: str = "bot_session",
) -> Client:
    """
    Создаёт MTProto клиент Pyrogram.

    :param api_id: Telegram API ID (получить на my.telegram.org)
    :param api_hash: Telegram API Hash (получить на my.telegram.org)
    :param bot_token: Токен бота
    :param proxy: Словарь с параметрами прокси, например:
                  {"scheme": "mtproto", "hostname": "...", "port": 443}
                  или для HTTP/SOCKS прокси:
                  {"scheme": "http", "hostname": "...", "port": 3128, "username": "...", "password": "..."}
    :param session_name: Имя сессии для хранения состояния
    :return: Экземпляр клиента Pyrogram
    """
    client_kwargs = {
        "name": session_name,
        "api_id": api_id,
        "api_hash": api_hash,
        "bot_token": bot_token,
        "parse_mode": ParseMode.HTML,
    }
    if proxy:
        client_kwargs["proxy"] = proxy

    return Client(**client_kwargs)


@asynccontextmanager
async def bot_context(
    api_id: int,
    api_hash: str,
    bot_token: str,
    proxy: dict | None = None,
    session_name: str = "bot_session",
):
    """Асинхронный контекстный менеджер для работы с клиентом."""
    client = create_client(api_id, api_hash, bot_token, proxy, session_name)
    await client.start()
    try:
        yield client
    finally:
        await client.stop()


async def send_message_in_channel(
    api_id: int,
    api_hash: str,
    bot_token: str,
    chat_id_channel: int | str,
    message: dict,
    proxy: dict | None = None,
    session_name: str = "bot_session",
):
    """
    Отправляет сообщение в канал через MTProto.

    :param api_id: Telegram API ID
    :param api_hash: Telegram API Hash
    :param bot_token: Токен бота
    :param chat_id_channel: ID канала (число или username через @)
    :param message: Словарь с сообщением (ключ "text")
    :param proxy: Параметры MTProto прокси
    :param session_name: Имя сессии
    """
    text = message.get("text", "")

    async with bot_context(api_id, api_hash, bot_token, proxy, session_name) as client:
        await client.send_message(
            chat_id=chat_id_channel,
            text=text,
            parse_mode=ParseMode.HTML,
        )


async def bot_info(
    api_id: int,
    api_hash: str,
    bot_token: str,
    proxy: dict | None = None,
    session_name: str = "bot_session",
) -> dict:
    """
    Получает информацию о боте через MTProto.

    :param api_id: Telegram API ID
    :param api_hash: Telegram API Hash
    :param bot_token: Токен бота
    :param proxy: Параметры MTProto прокси
    :param session_name: Имя сессии
    :return: Информация о боте (User dict)
    """
    async with bot_context(api_id, api_hash, bot_token, proxy, session_name) as client:
        return client.me
