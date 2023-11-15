# ShellBot
### Telegram bot that will run commands in your shell

## Quick start
```shell
pip install -r requirements.txt
# configuring config.json...
python main.py
```

## Configuration
Config is a `config.json` file.

Here is an example:
![This config in an actual bot](https://github.com/barabum0/shell-bot/blob/main/example-recording.gif?raw=true)

```json
{
  "bot_token": "1234567890:AAAAAAAAAAAAAAAASOMETOKENAAAAAAAA",
  "whitelisted_chat_ids": [],
  "shells": {
    "/get_root_dir": {
      "shell": "ls /",
      "send_output": true,
      "output_message": "Done, here is your root directory:",
      "loading_message": "Processing\\.\\.\\.",
      "description": "Get contents of the root directory",
      "need_confirmation": false
    },
    "/update_backend": {
      "shell": "echo \"🔮 Imagine this is a backend update command...\"",
      "send_output": true,
      "output_message": "Your backend was just updated\\!",
      "loading_message": "Updating\\.\\.\\.",
      "description": "Update backend",
      "need_confirmation": true
    }
  },
  "default_commands": {
    "/help": true
  }
}
```

### Config insides

- `bot_token` - Your telegram bot token
- `whitelisted_chat_ids` - Chat IDs where bot will work. Everywhere if empty
- `shells` - A list of your commands. Key is a command and value is an object with this parameters:
  - `shell` - Command. (`ls`, `echo "asdasd"`, etc.)
  - `send_output` - boolean. Send output of the command?
  - `output_message` - Message that will be shown after command execution
  - `loading_message` - Message that will be shown while command execution
  - `description` - Description of the command that will be shown in `/help`
  - `need_confirmation` - boolean. Execution needs confirmation?
- `default_commands` - Enable / Disable default commands. Currently there is only one - `/help`

**Note that `output_message`, `loading_message` and `description` are markdown strings so they should be escaped.**