import os
import re
import subprocess

from aiogram import Bot, F, Router, exceptions
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from loguru import logger

from shell_bot.config import Config, defaults

router = Router()


@router.message(
    F.func(lambda message: message.text.startswith("/") and not any(message.text.startswith(d) for d in defaults))
)
async def custom_command(
    message: Message, config: Config, bot: Bot, state: FSMContext, is_confirmed: bool = False
) -> None:
    assert message.text is not None

    # Check if chat is whitelisted and mention check for non-private chats is skipped for simplicity
    if config.whitelisted_chat_ids and message.chat.id not in config.whitelisted_chat_ids:
        logger.error("Chat {chat_id} not in whitelisted chats", chat_id=message.chat.id)
        return

    if config.prevent_unmentioned_commands_in_groups and message.chat.type != "private" and not is_confirmed:
        me = await bot.get_me()
        if not message.text.split(" ", maxsplit=1)[0].endswith(f"@{me.username}"):
            return

    # Extract command text
    command_text = re.match(r"/[^@\s\W]+", message.text)
    if not command_text:
        logger.error('"{text}" is not a valid command', text=message.text)
        return

    command_text_match = command_text.group()
    command = config.shells.get(command_text_match)
    assert command is not None

    logger.info("command text: {}".format(command_text_match))

    # Handle command confirmation if needed
    if command.need_confirmation and not is_confirmed:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Yes", callback_data=f"confirm_yes"),
                    InlineKeyboardButton(text="⛔️ No", callback_data=f"confirm_no"),
                ]
            ]
        )
        await state.set_data({"original_message": message.text})
        await message.reply(f"Are you sure you want to run `{command_text_match}`?", reply_markup=keyboard)
        return

    assert message.text is not None

    loading_message = await bot.send_message(message.chat.id, command.loading_message, parse_mode="Markdown")

    # Execute the command
    try:
        result = subprocess.run(
            [f"{command.shell}"] + message.text.split(" ")[1:],
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        result_text = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        result_text = e.stderr.strip()

    if command.send_output:
        output_with_result = f"{command.output_message}\n\n```\n{result_text}\n```"
    else:
        output_with_result = command.output_message

    try:
        await loading_message.delete()
    except:
        pass

    try:
        await bot.send_message(message.chat.id, output_with_result, parse_mode="Markdown")
    except exceptions.TelegramBadRequest:
        await bot.send_document(
            message.chat.id, BufferedInputFile(result.encode(), "output.txt"), caption=command.output_message
        )


@router.callback_query(F.data.startswith("confirm_"))
async def confirm_command(callback_query: CallbackQuery, config: Config, bot: Bot, state: FSMContext) -> None:
    assert isinstance(callback_query.message, Message)
    assert callback_query.data is not None

    if config.whitelisted_chat_ids and callback_query.message.chat.id not in config.whitelisted_chat_ids:
        return

    _, choice = callback_query.data.split("_", maxsplit=1)
    await callback_query.message.delete()

    data = await state.get_data()

    if choice == "yes":
        message = callback_query.message
        md = message.dict()
        md.pop("text")
        message = Message(text=data.get("original_message"), **md)
        await custom_command(message, config, bot, state, is_confirmed=True)
