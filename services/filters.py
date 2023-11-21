def build_command_regex(commands: list[str]) -> str:
    commands_or = "|".join(commands)
    final_regex = f"(?P<command>{commands_or})"
    return final_regex
