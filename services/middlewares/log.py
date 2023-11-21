from typing import Optional, Type, Any

from aiogram.client.session.middlewares.base import BaseRequestMiddleware, NextRequestMiddlewareType
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType, Response
from loguru import logger


class RequestLogging(BaseRequestMiddleware):
    def __init__(self, ignore_methods: Optional[list[Type[TelegramMethod[Any]]]] = None):
        """
        Middleware for logging outgoing requests

        :param ignore_methods: methods to ignore in logging middleware
        """
        self.ignore_methods = ignore_methods if ignore_methods else []

    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[TelegramType],
        bot: "Bot",
        method: TelegramMethod[TelegramType],
    ) -> Response[TelegramType]:
        if type(method) not in self.ignore_methods:
            logger.info(
                "Request with method={method} by bot id={bot_id}",
                method=type(method).__name__,
                bot_id=bot.id,
            )
        return await make_request(bot, method)
