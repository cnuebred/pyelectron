from ...core.parser.parser_node import Command_Parser
from ...settings import PREFIX


async def on_message_node(message):
    if message.content.startswith(PREFIX):
        await Command_Parser(message).parser()
        return
