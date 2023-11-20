import asyncio

from aiogram import Bot, Dispatcher
from loguru import logger

from services.config import load_config
from services.routers import custom, default


async def setup() -> tuple[Bot, Dispatcher]:
    _config = load_config()
    _bot = Bot(token=_config.bot_token, parse_mode="MarkdownV2")
    _dispatcher = Dispatcher(config=_config)

    _routers = [
        custom.router,
        default.router
    ]
    _dispatcher.include_routers(*_routers)
    return _bot, _dispatcher


if __name__ == '__main__':
    logger.info("Starting bot...")
    bot, dispatcher = asyncio.run(setup())
    dispatcher.run_polling(bot)
    logger.info("Stopped!")