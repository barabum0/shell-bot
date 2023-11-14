import json
from typing import Annotated
from annotated_types import Predicate
from pydantic import BaseModel, Field

SlashCommand = Annotated[str, Predicate(lambda x: x.startswith("/") and "/" not in x[1:])]


class DefaultCommands(BaseModel):
    help: bool = Field(alias="/help", default=True)


class Shell(BaseModel):
    shell: str
    send_output: bool = False
    output_message: str = "Done!"


class Config(BaseModel):
    bot_token: str
    whitelisted_chat_ids: list[int] = []
    shells: dict[SlashCommand, Shell]
    default_commands: DefaultCommands = DefaultCommands()


def load_config(path: str = "config.json") -> Config:
    with open(path, "r") as file:
        config = Config(**json.load(file))

    return config
