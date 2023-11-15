from aiogram import Router, F
from aiogram.types import Message

from services.config import config

router = Router()


@router.message(F.text.startswith("/help") & config.default_commands.help)
async def help_command(message: Message):
    text = "*Your shells:*\n\n"
    text += "\n".join(
        f"\- `{k}`\n{v.description}" for k, v in config.shells.items()
    )
    await message.reply(text)
