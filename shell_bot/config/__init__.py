import json
from typing import Annotated

import yaml
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


def load_config_json(path: str = "config.json") -> Config:
    with open(path, "r") as file:
        config = Config.model_validate(json.load(file))

    return config


def load_config_yaml(path: str = "config.yaml") -> Config:
    with open(path, "r") as file:
        config = Config.model_validate(yaml.safe_load(file))

    return config


def load_config(path) -> Config:
    if path.endswith(".yaml"):
        return load_config_yaml(path)
    elif path.endswith(".json"):
        return load_config_json(path)

    raise ValueError("Config should be either .yaml or .json")
