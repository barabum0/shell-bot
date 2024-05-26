import os
import re

from aiogram import Router, F, Bot, exceptions
from aiogram.types import Message, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from services.config import Config, defaults

router = Router()


@router.message(F.func(
        lambda message: message.text.startswith("/") and not any(message.text.startswith(d) for d in defaults)
))
async def custom_command(message: Message, config: Config, bot: Bot, is_confirmed: bool = False) -> None:
    # Check if chat is whitelisted and mention check for non-private chats is skipped for simplicity
    if config.whitelisted_chat_ids and message.chat.id not in config.whitelisted_chat_ids:
        logger.error("Chat {chat_id} not in whitelisted chats", chat_id=message.chat.id)
        return

    if config.prevent_unmentioned_commands_in_groups and message.chat.type != "private" and not is_confirmed:
        me = await bot.get_me()
        if not message.text.split(' ', maxsplit=1)[0].endswith(f"@{me.username}"):
            return

    # Extract command text
    command_text = re.match(r"/[^@\s\W]+", message.text)
    if not command_text:
        logger.error("\"{text}\" is not a valid command", text=message.text)
        return

    logger.info("command text: {}".format(command_text.group()))

    command_text = command_text.group()
    command = config.shells.get(command_text)

    # Handle command confirmation if needed
    if command.need_confirmation and not is_confirmed:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Yes", callback_data=f"confirm_yes_{command_text}"),
             InlineKeyboardButton(text="⛔️ No", callback_data=f"confirm_no_{command_text}")]
        ])
        await message.reply(f"Are you sure you want to run `{command_text}`?", reply_markup=keyboard)
        return

    # Execute the command
    result = os.popen(f"{command.shell} {message.text.split(' ', maxsplit=1)[1]}".strip()).read().strip()
    if command.send_output:
        output_with_result = f"{command.output_message}\n\n```\n{result}\n```"
    else:
        output_with_result = command.output_message

    try:
        await bot.send_message(message.chat.id, output_with_result, parse_mode='Markdown')
    except exceptions.TelegramBadRequest:
        await bot.send_document(message.chat.id, BufferedInputFile(result.encode(), "output.txt"), caption=command.output_message)


@router.callback_query(F.data.startswith("confirm_"))
async def confirm_command(callback_query, config: Config, bot: Bot) -> None:
    if config.whitelisted_chat_ids and callback_query.message.chat.id not in config.whitelisted_chat_ids:
        return

    _, choice, *command_text = callback_query.data.split("_")
    command_text = "_".join(command_text)
    await callback_query.message.delete()

    if choice == "yes":
        message = callback_query.message
        md = message.dict()
        md.pop("text")
        message = Message(text=command_text, **md)
        await custom_command(message, config, bot, is_confirmed=True)
