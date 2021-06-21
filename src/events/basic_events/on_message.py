from ..create_events.on_member_join import on_member_join
from ..create_events.experience import LevelSystem
from ...core.parser.parser_node import CommandParser
from ...settings import PREFIX


async def on_message_node(message):
    if str(message.type) == "MessageType.new_member":
        await on_member_join(message)
    if message.content.startswith(PREFIX):
        await CommandParser(message).parser()
        return
    if str(message.channel.type) != "private":
        await LevelSystem().add_experience(message)
