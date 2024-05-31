from aiogram import Bot, F, Router
from aiogram.types import Message
from loguru import logger

from shell_bot.config import Config

router = Router()


@router.message(F.text.startswith("/help"))
async def help_command(message: Message, config: Config, bot: Bot) -> None:
    if not config.default_commands.help:
        logger.error("/help was called but is not enabled")
        return
    me = await bot.get_me()
    assert me.username is not None

    text = "*Your shells:*\n\n"
    text += "\n".join(
        f"\\- `{k}{f"@{me.username}" if config.prevent_unmentioned_commands_in_groups else ""}`\n{v.description}"
        for k, v in config.shells.items()
    )
    await message.reply(text)
