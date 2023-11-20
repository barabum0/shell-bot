import asyncio

from aiogram import Bot, Dispatcher
from loguru import logger

from services.config import load_config
from services.routers import custom, default

config = load_config()
bot = Bot(token=config.bot_token, parse_mode="MarkdownV2")
dispatcher = Dispatcher(config=config)


async def setup() -> None:
    routers = [
        custom.router,
        default.router
    ]
    dispatcher.include_routers(*routers)


if __name__ == '__main__':
    logger.info("Starting bot...")
    asyncio.run(setup())
    dispatcher.run_polling(bot)
    logger.info("Stopped!")