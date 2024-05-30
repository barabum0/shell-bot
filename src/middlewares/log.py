from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot
from aiogram.types import Update
from loguru import logger


class UpdateLogging(BaseMiddleware):
    def __init__(self):
        """
        Middleware for logging updates
        """

    async def __call__(
        self, handler: Callable[[Update, dict[str, Any]], Awaitable[Any]], event: Update, data: dict[str, Any]
    ) -> Any:
        logger.info("Update with id{update_id}", update_id=event.update_id)
        return await handler(event, data)
