import re

import discord
from discord.embeds import Embed

from ..core.database.postgres_controller import ControllerPostgres

from ..utils import log
from .command_node import command_exe

FORM_SEPARATOR = ";;"
FORM_EMOJIS = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"]

EMBED_RE = r"(?P<selector>\w+?)(?<=[^\\])<(?P<content>.+?)(?<=[^\\])>"
EMBED_FIELD_RE = r"(?P<name>.+?)(?<=[^\\]);;(?P<value>.+)"
EMBED_SPECIFIC = {"footer": "text", "image": "url", "author": "name"}


@command_exe
async def form(message, params, **options):
    values = " ".join(params).strip()
    values = values.split(FORM_SEPARATOR)

    if len(values) > 10:
        return log((["b", "w"], "too many arguments"))

    title = values[0]
    form_options = [option for option in values[1:] if option]

    if not title:
        return log((["b", "w"], "not enough arguments"))

    embed_message = Embed()
    embed_message.description = f"📊 **{title}**\n\n"
    embed_message.colour = discord.Colour.from_rgb(77, 119, 215)
    embed_message.set_footer(text=f"by {message.author}")

    if not form_options:
        message_form = await message.channel.send(embed=embed_message)
        for emoji in ["✅", "❌"]:
            await message_form.add_reaction(emoji)
        return

    ziped_options = list(zip(FORM_EMOJIS, form_options))

    for number, desc in ziped_options:
        embed_message.description += f"{number} {desc}\n"

    message_form = await message.channel.send(embed=embed_message)

    for number in range(len(form_options)):
        await message_form.add_reaction(FORM_EMOJIS[number])


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


# @command_exe # - removed tmp
async def embed(message, params, **options):
    data = re.findall(EMBED_RE, " ".join(params))

    embed_object = {}

    for selector, content in data:

        if selector == "field":
            name = "•"
            value = content
            if content := re.search(EMBED_FIELD_RE, content):
                name = content.group("name")
                value = content.group("value")

            name = name.replace("\\", "")
            value = value.replace("\\", "")
            content = {"name": name, "value": value}

            if not embed_object.get("fields"):
                embed_object["fields"] = [content]
            else:
                embed_object["fields"].append(content)
            continue

        content = content.replace("\\", "")

        for key, value in EMBED_SPECIFIC.items():
            if selector == key:
                embed_object[key] = {value: content}
                continue

        embed_object.update({selector: content})

    try:
        embed_message = Embed().from_dict(embed_object)
        await message.channel.send(embed=embed_message)
    except discord.errors.HTTPException:
        log((["b", "w"], "wrong data selectors"))
