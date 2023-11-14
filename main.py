import asyncio

from aiogram import Bot

from services.config import load_config

config = load_config()
bot = Bot(token=config.bot_token, parse_mode="MarkdownV2")


async def main() -> None:
    pass


if __name__ == '__main__':
    asyncio.run(main())