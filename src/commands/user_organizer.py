from collections import defaultdict

from discord.embeds import Embed

from ..core.database.mongo_controller import Controller_mongo
from .command_node import command_exe


@command_exe
async def help(message, params):
    list_of_commands = Controller_mongo(_collection="config").load(
        _filter={"category": "commands"}, _folder="commands"
    )
    commands_by_permission = defaultdict(list)

    def command_key(command, properties):
        commands_by_permission[properties.get("permission")].append(f"`{command}`")

    [
        command_key(command, properties)
        for command, properties in list_of_commands.items()
    ]

    set_description = ""
    for permission, property in commands_by_permission.items():
        set_description += f"""**Commands for {permission}**
        {'**,** '.join(property)}
        """

    set_description += """**For more information**
        enter the selected command with a note `--help`
        > **Sample:**
        > `;help --help`
        """

    embed = Embed(title="List of available commands", description=set_description)
    await message.channel.send(embed=embed)


@command_exe
async def details(message, command, command_data):
    embed = Embed(title=command, description=command)
    embed.add_field(
        name=command_data.get("permission"),
        value=command_data.get("description").get("pl"),
    )
    await message.channel.send(embed=embed)
