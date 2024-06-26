<div align="center">

# ShellBot

![GitHub stars](https://img.shields.io/github/stars/barabum0/shell-bot)
![GitHub forks](https://img.shields.io/github/forks/barabum0/shell-bot)
![GitHub issues](https://img.shields.io/github/issues/barabum0/shell-bot)
![GitHub license](https://img.shields.io/github/license/barabum0/shell-bot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Formatted with: isort](https://img.shields.io/badge/formatted%20with-isort-blue.svg)](https://github.com/psf/black)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

</div>

## About 🤖

ShellBot is a Telegram bot designed to run commands in a shell environment. It allows users to execute predefined shell commands through a Telegram interface, making it a versatile tool for remote command execution.

<div align="center">
    <img src="https://github.com/barabum0/shell-bot/blob/main/example-recording.gif?raw=true" width="50%" height="50%">
</div>

## Installation 🛠️

To install ShellBot, install it with [`pipx`](https://github.com/pypa/pipx?tab=readme-ov-file):

```bash
pipx install git+https://github.com/barabum0/shell-bot@pipx
```

## Usage 🚀

1. Create a `config.json` or `config.yaml` file based on the `config_example.json` or `config_example.yaml`. The bot can read both formats.
2. Add your Telegram bot token and other configuration details to the file.
3. Run the bot using:

```bash
shellbot
```

By default, it will use the `config.json` file, but you can specify another file with:

```bash
shellbot --config config1.yaml
```

## Troubleshooting 🔍

If you encounter any issues while using ShellBot, please check the [GitHub Issues](https://github.com/barabum0/shell-bot/issues) page for similar problems or to open a new issue.

## Contribution 🤝

Contributions are welcome. Please fork the repository, make your changes, and submit a pull request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
