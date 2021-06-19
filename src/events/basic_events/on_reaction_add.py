from ..create_events.add_role_by_reaction import add_role_by_reaction


async def on_reaction_add(data):
    await add_role_by_reaction(data)
