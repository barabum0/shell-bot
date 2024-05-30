import json
from typing import Annotated

from annotated_types import Predicate
from pydantic import BaseModel, Field

defaults = ["/help"]
SlashCommand = Annotated[str, Predicate(lambda x: x.startswith("/") and "/" not in x[1:] and x not in defaults)]


class DefaultCommands(BaseModel):
    help: bool = Field(alias="/help", default=True)


class Shell(BaseModel):
    shell: str
    send_output: bool = False
    output_message: str = "Done!"
    loading_message: str = "Processing..."
    description: str = "Some script"
    need_confirmation: bool = False


class Config(BaseModel):
    bot_token: str
    whitelisted_chat_ids: list[int] = []
    prevent_unmentioned_commands_in_groups: bool = True
    shells: dict[SlashCommand, Shell]
    default_commands: DefaultCommands = DefaultCommands()

    @property
    def custom_commands(self) -> list[str]:
        return list(self.shells.keys())


def load_config(path: str = "config.json") -> Config:
    with open(path, "r") as file:
        config = Config(**json.load(file))

    return config
