import os

import regex
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from loguru import logger

from services.config import Config, defaults
from services.routers import escape_markdown

router = Router()


@router.message(
    F.func(
        lambda message: message.text.startswith("/") and not any(message.text.startswith(d) for d in defaults)
    )
)
async def custom_command(
        message: Message = None,
        config: Config = None,
        confirmed: bool = False,
        confirmation_message: Message = None,
        confirmation_command: str = None) -> None:
    if config.whitelisted_chat_ids and message.chat.id not in config.whitelisted_chat_ids:
        logger.error("{chat_id} not in whitelisted chats", chat_id=message.chat.id)
        return

    if not confirmation_command:
        command_text = regex.match("(?P<command>/[^@ ]*)", message.text).group("command")
    else:
        command_text = confirmation_command
    command = config.shells.get(command_text)

    if command.need_confirmation and not confirmed:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="✅ Yes", callback_data=f"confirm_yes_{command_text}"),
            InlineKeyboardButton(text="⛔️ No", callback_data=f"confirm_no_{command_text}")
        ]])

        await message.reply(f"*Are you sure you want to run *`{message.text}`*?*", reply_markup=keyboard)
        return
    elif command.need_confirmation and confirmed:
        m = confirmation_message
        await m.edit_text(command.loading_message)
    else:
        m = await message.reply(command.loading_message)

    result = os.popen(command.shell).read()
    output = f"{command.output_message}"

    result = escape_markdown(result)
    if command.send_output:
        output_with_result = f"{output}\n\n```shell\n{result}\n```"
    else:
        output_with_result = output

    try:
        await m.edit_text(output_with_result)
    except TelegramBadRequest:
        await m.delete()
        await m.reply_document(document=BufferedInputFile(result.encode("utf-8"), filename="output.txt"), caption=output)


@router.callback_query(F.data.startswith(f"confirm_"))
async def confirm_command(callback_query: CallbackQuery, config: Config):
    if config.whitelisted_chat_ids and callback_query.chat.id not in config.whitelisted_chat_ids:
        return

    _, choice, *command = callback_query.data.split("_")

    command = "_".join(command)
    if choice == "no":
        await callback_query.message.delete()
        return

    if choice == "yes":
        return await custom_command(confirmed=True,
                                    confirmation_message=callback_query.message,
                                    confirmation_command=command, config=config)
