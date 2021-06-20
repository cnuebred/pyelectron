from ...core.database.postgres_controller import ControllerPostgres
from datetime import datetime


async def on_guild_join_node(guild):
    guilds_database = ControllerPostgres("guilds")
    guilds_database.insert(
        values=[
            str(guild.id),
            str(guild.name.replace("'", "''")),
            str(guild.owner_id),
            str(datetime.now()),
            str(guild.created_at),
        ]
    )
