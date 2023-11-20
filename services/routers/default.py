from aiogram import Router, F
from aiogram.types import Message

from services.config import Config

router = Router()


@router.message(F.text.startswith("/help") & F.config.default_commands.help)
async def help_command(message: Message, config: Config):
    text = "*Your shells:*\n\n"
    text += "\n".join(
        f"\- `{k}`\n{v.description}" for k, v in config.shells.items()
    )
    await message.reply(text)
