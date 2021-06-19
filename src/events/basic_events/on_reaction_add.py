from ..create_events.add_config_role_by_reaction import add_config_role_by_reaction


async def on_reaction_add(data):
    print(data.message_id)
    print(data.user_id)
    print(data.channel_id)
    print(data.guild_id)
    print(data.emoji)
    print(data.member)
    add_config_role_by_reaction()
