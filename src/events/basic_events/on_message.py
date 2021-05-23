from ...core.parser.parser_node import CommandParser
from ...settings import PREFIX


async def on_message_node(message):
    if message.content.startswith(PREFIX):
        await CommandParser(message).parser()
        return
