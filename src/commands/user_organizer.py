from discord.embeds import Embed


from ..core.database.postgres_controller import ControllerPostgres
from .command_node import command_exe


def set_description(description):  # TODO
    return ""


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
        value=f"> {description_profile}",
        inline=True,
    )

    await message.channel.send(embed=message_embed)
