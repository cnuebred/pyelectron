import re

import psycopg2

from ..core.mockdata import COMMANDS

from ..core.database.postgres_controller import ControllerPostgres

from ..utils import log
from .command_node import command_exe


@command_exe
async def emoji_s(message, params, **options):
    if len(vertical_params := (message.content.split("\n"))) < 2:
        return
    emoji_index = 1
    print(vertical_params[0])

    if base_emoji_settings := re.findall(r"(\d{18})", vertical_params[0]):
        emoji_index = 0

    print(base_emoji_settings)
    vertical_params = vertical_params[1:]

    if len(vertical_params) != len(message.role_mentions):
        return

    emoji_base = ControllerPostgres("config_role_by_reaction")

    for param in vertical_params:
        param = param.split()

        if (
            len(param) == 3
            and base_emoji_settings
            or (len(param) == 2 and not base_emoji_settings)
        ):
            continue

        if bool(emoji_index) and len(message_id := param[0]) != 18:
            continue

        try:
            message_id = base_emoji_settings[0]
        except IndexError:
            log((["b", "w"], "non base massege"))
        try:
            channel_id = base_emoji_settings[1]
        except IndexError:
            channel_id = message.channel.id
            log((["b", "w"], "non base channel"))

        emoji = (
            param[emoji_index]
            if len(param[emoji_index]) < 18
            else re.findall(r"(\d+)", param[emoji_index])[0]
        )
        role_id = param[-1][3:-1]

        print(message_id, emoji, role_id)
        try:

            emoji_base.insert(
                values=[
                    str(message_id),
                    str(channel_id),
                    str(message.guild.id),
                    str(emoji),
                    str(role_id),
                ]
            )
        except psycopg2.errors.InFailedSqlTransaction:
            log((["b", "f"], "duplicate values"))


@command_exe
async def refresh_db(message, params, **options):
    for command_name in COMMANDS.keys():
        command_exe(command_name)
