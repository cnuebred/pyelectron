from collections import defaultdict
from typing import Text

from discord.embeds import Embed

from ..core.database.postgres_controller import ControllerPostgres
from .command_node import command_exe


@command_exe
async def help(message, params, **options):
    pg_commands = ControllerPostgres(table="config_commands")
    all_permissions = pg_commands.load(
        selector="DISTINCT command_permission", join=True
    )

    set_description = ""
    for permission in all_permissions:
        commands_on_permission = pg_commands.load(
            selector="command_name",
            condition=f"command_permission = '{permission}'",
            join=True,
        )

        set_description += f"""**Commands for {permission}**
        {'**,** '.join([f"`{command}`" for command in commands_on_permission])}
        """

    set_description += """**For more information**
        Enter the selected command with a note `--help`
        > **Sample:**
        > `;help --help`
        """

    embed = Embed(title="List of available commands", description=set_description)
    await message.channel.send(embed=embed)


@command_exe
async def details(message, command, **options):
    embed = Embed(title=command, description=command)
    if not (command_data := options.get("command_data")):
        return

    permission_note = (
        f"**Permission -** {perm}"
        if (perm := command_data.get("command_permission"))
        else "Here be dragons"
    )
    description_note = (
        desc if (desc := command_data.get("description_pl")) else "Here be dragons too"
    )

    embed.add_field(
        name=permission_note,
        value=description_note,
    )
    await message.channel.send(embed=embed)
