from ..create_events.remove_role_by_reaction import remove_role_by_reaction


async def on_reaction_remove(bot, data):
    await remove_role_by_reaction(bot, data)
