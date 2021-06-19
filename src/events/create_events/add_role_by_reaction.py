from ...core.database.postgres_controller import ControllerPostgres


async def add_role_by_reaction(data):
    if not data.member:
        return
    emoji = data.emoji.id if data.emoji.id else data.emoji.name

    emoji_table = ControllerPostgres("config_role_by_reaction")
    roles_id = emoji_table.load(
        condition=f"message_id='{data.message_id}' AND guild_id='{data.guild_id}' AND channel_id='{data.channel_id}' AND emoji_id='{emoji}'",
        selector="role_id",
        join=True,
    )

    async def add_role_to_member(role_id):
        role = data.member.guild.get_role(int(role_id))
        await data.member.add_roles(role)

    roles_id = [await add_role_to_member(role_id) for role_id in roles_id]
