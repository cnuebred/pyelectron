import re

from discord.embeds import Embed

from ..core.database.postgres_controller import ControllerPostgres
from .command_node import command_exe


def set_description(description):
    regex = r"(?P<key_>\w*(?=\())(?:\()(?P<value_>.+?)(?:\))"
    result_str = ""
    if not description:
        description = ""

    def key_(part):
        result_regex = re.search(pattern=regex, string=part)
        if not result_regex:
            return "•"
        return f"[{result_regex.group('key_')}]({result_regex.group('value_')})"

    result_str = " | ".join(
        [
            result_part
            for part in description.split(",")
            if (result_part := key_(part)) and part
        ]
    )

    return result_str if result_str else "**•**"


@command_exe
async def profile(message, params, **options):
    user_data = ControllerPostgres(table="user_profile")
    user_data = user_data.load(
        condition=f"guild_id = '{message.guild.id}' AND user_id = '{message.author.id}'"
    )
    if not user_data:
        return
    user_data = user_data[0]

    member = await message.guild.fetch_member(int(message.author.id))

    description_profile = set_description(user_data["description"])

    message_embed = Embed(description=f"Profile <@{message.author.id}>")
    message_embed.set_thumbnail(url=message.author.avatar_url)
    message_embed.add_field(
        name="Level Data",
        value=f"**experience**: {user_data['experience_user']}\n**level**: {user_data['level_user']}",
        inline=True,
    )
    message_embed.add_field(
        name="Joined At",
        value=f"```{member.joined_at.strftime('%Y/%m/%d %H:%M:%S')}```",
        inline=True,
    )
    message_embed.add_field(
        name="Messages",
        value=f"```{user_data['messages']}```",
        inline=True,
    )
    message_embed.add_field(
        name="Links",
        value=f"{description_profile}",
        inline=True,
    )

    await message.channel.send(embed=message_embed)


@command_exe
async def account(message, params, **options):
    if params:
        code = params[0]
        login_base = ControllerPostgres("pyelectron_service_login")
        login_base.update(
            columns=["user_id"],
            values=[message.author.id],
            condition=f"verify_code = {code.strip()}",
        )
        id_value = login_base.load(
            selector="user_id", condition=f"verify_code = {code.strip()}"
        )
        print(id_value)
        embed_message = Embed(
            description="Successfully verified\nThank you for joined to us"
        )
        return await message.channel.send(embed=embed_message)

    embed_message = Embed(title="Create Account")
    embed_message.description = (
        "[👆 click here](http://site) to create account on **pyElectron Service**"
    )
    await message.channel.send(embed=embed_message)


@command_exe
async def top(message, params, **options):
    member_limit = int(params[0]) if params else 10
    if member_limit > 20:
        member_limit = 20

    member_profile_controller = ControllerPostgres(table="user_profile")
    top_members = member_profile_controller.load(
        order_by="messages",
        limit=str(member_limit),
        order_by_descending=True,
    )

    embed_message = Embed(title=f"Top {len(top_members)} members:")

    for index, user_data in enumerate(top_members, 1):
        member = message.guild.get_member(int(user_data[1]))
        member_nick_tag = f"{member.name}#{member.discriminator}"
        member_messages_amount = user_data[4]

        embed_message.add_field(
            name=f"{index}. {member_nick_tag}",
            value=f"{member_messages_amount}",
            inline=False,
        )

    return await message.channel.send(embed=embed_message)
