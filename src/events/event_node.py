from .basic_events.on_reaction_remove import on_reaction_remove
from .basic_events.on_reaction_add import on_reaction_add
from .basic_events.on_guild_join import on_guild_join_node
from .basic_events.on_guild_remove import on_guild_remove_node
from .basic_events.on_message import on_message_node
from .basic_events.on_ready import on_ready_node


def event_node(bot):
    @bot.event
    async def on_ready():
        await on_ready_node()

    @bot.event
    async def on_message(message):
        await on_message_node(message)

    @bot.event
    async def on_raw_reaction_add(data):
        await on_reaction_add(data)

    @bot.event
    async def on_raw_reaction_remove(data):
        await on_reaction_remove(bot, data)

    @bot.event
    async def on_guild_join():
        await on_guild_join_node()

    @bot.event
    async def on_guild_remove():
        await on_guild_remove_node()
