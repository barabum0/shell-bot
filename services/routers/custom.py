import os

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, BufferedInputFile

from services.config import config
from services.routers import escape_markdown

router = Router()


@router.message(F.text.in_(config.custom_commands))
async def custom_command(message: Message) -> None:
    command = config.shells.get(message.text)

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
        await message.reply_document(document=BufferedInputFile(result.encode("utf-8"), filename="output.txt"), caption=output)
