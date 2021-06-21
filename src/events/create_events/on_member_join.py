from ...core.database.postgres_controller import ControllerPostgres


async def on_member_join(message):
    role_id = ControllerPostgres("config_role_on_join").load(
        condition=f"guild_id='{message.guild.id}'", selector="role_id", join=True
    )
    if roles := [int(role_id_) for role_id_ in role_id if role_id_]:
        for role_ in roles:
            role = message.guild.get_role(role_)
            await message.author.add_roles(role)
