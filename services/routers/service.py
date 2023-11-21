from aiogram import Router, Bot

from services.config import Config

router = Router()


# @router.startup()
# async def on_startup(config: Config, bot: Bot) -> None:
#     for white_id in config.whitelisted_chat_ids:
#         await bot.send_message(chat_id=white_id, text="TEST")
