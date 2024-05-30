from aiogram import F, Router
from aiogram.types import Message
from loguru import logger

from src.config import Config

router = Router()


@router.message(F.text.startswith("/help"))
async def help_command(message: Message, config: Config):
    if not config.default_commands.help:
        logger.error("/help was called but is not enabled")
        return
    text = "*Your shells:*\n\n"
    text += "\n".join(f"\- `{k}`\n{v.description}" for k, v in config.shells.items())
    await message.reply(text)
