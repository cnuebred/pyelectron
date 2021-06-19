from ...core.database.postgres_controller import ControllerPostgres


async def remove_role_by_reaction(bot, data):
    member = await bot.get_guild(data.guild_id).fetch_member(data.user_id)
    if not member:
        return

    emoji = data.emoji.id if data.emoji.id else data.emoji.name
    emoji_table = ControllerPostgres("config_role_by_reaction")
    roles_id = emoji_table.load(
        condition=f"message_id='{data.message_id}' AND guild_id='{data.guild_id}' AND channel_id='{data.channel_id}' AND emoji_id='{emoji}'",
        selector="role_id",
        join=True,
    )

    async def remove_role_to_member(role_id):
        role = member.guild.get_role(int(role_id))
        await member.remove_roles(role)

    roles_id = [await remove_role_to_member(role_id) for role_id in roles_id]
