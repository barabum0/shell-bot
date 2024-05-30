import re


def escape_markdown(text):
    """
    Escapes markdown special characters: \ ` * _ { } [ ] ( ) # + - . !
    """
    markdown_characters = r"\\`*_{}[]()#+-.!"
    return re.sub(r'([{}])'.format(markdown_characters), r'\\\1', text)
