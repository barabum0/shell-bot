from typing import Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Update


class ParamMiddleware(BaseMiddleware):
    def __init__(self, key: str, param: Any):
        """
        Middleware for adding custom update params
        """
        self.param = param
        self.key = key

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any]
    ) -> Any:
        data[self.key] = self.param
        return await handler(event, data)
