import asyncio

from aiogram import Bot, Dispatcher

from services.config import load_config
from services.routers import custom

config = load_config()
bot = Bot(token=config.bot_token, parse_mode="MarkdownV2")
dispatcher = Dispatcher()


async def setup() -> None:
    dispatcher.include_router(custom.router)


if __name__ == '__main__':
    asyncio.run(setup())
    dispatcher.run_polling(bot)