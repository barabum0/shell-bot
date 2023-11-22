import click
from aiogram import Bot, Dispatcher
from loguru import logger

from services.config import load_config
from services.middlewares.log import UpdateLogging
from services.routers import custom, default, service


def setup(config_path: str) -> tuple[Bot, Dispatcher]:
    _config = load_config(config_path)
    _bot = Bot(token=_config.bot_token, parse_mode="MarkdownV2")
    _dispatcher = Dispatcher(config=_config)
    _dispatcher.update.middleware(UpdateLogging())

    _routers = [
        custom.router,
        default.router,
        service.router
    ]
    _dispatcher.include_routers(*_routers)
    return _bot, _dispatcher


@click.command()
@click.option('--config', default='config.json', help='Path to the configuration file.', type=click.Path(exists=True, dir_okay=False))
def main(config):
    logger.info("Loading config from {config}...", config=config)
    logger.info("Starting bot...")
    bot, dispatcher = setup(config)
    dispatcher.run_polling(bot)
    logger.info("Stopped!")


if __name__ == '__main__':
    main()
