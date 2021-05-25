from ...commands import *
from ...settings import BOT_OWNER, PREFIX
from ...utils import is_member, log
from ..database.postgres_controller import ControllerPostgres


class CommandParser:
    def __init__(self, message) -> None:
        content_array = message.content.strip().split()
        self.message = message
        self.command = content_array[0][len(PREFIX) :]
        self.params = content_array[0:]
        self.channel_type = str(message.channel.type)
        self.guild = message.guild or None

    async def _get_user_permission(self, target_permission):
        if target_permission == "user":
            return True

        member = await is_member(self.message.author, self.guild)
        if not member:
            return log((["b", "bl"], "The member does not exist"))

        if str(member.id) == BOT_OWNER:
            return True

        if target_permission != "owner" and int(member.id) == int(self.guild.owner_id):
            return True

        message_author_permission = [str(role.id) for role in member.roles]
        command_permission = ControllerPostgres(table="guild_config_roles").load(
            condition=f"guild_id = '{str(self.guild.id)}' AND command_name = '{self.command}'",
            selector="role_id",
        )

        shared_permissions = [
            permission["role_id"]
            for permission in command_permission
            if permission["role_id"] in message_author_permission
        ]

        if not shared_permissions:
            return False

        return True

    def _check_channel_type(self, target_channel):
        if target_channel in ["text", "news"]:
            target_channel = "guild"

        if target_channel == "all":
            return True
        if target_channel == self.channel_type:
            return True

        return False

    async def parser(self):

        if not (command_data := COMMANDS.get(self.command)):
            return

        if not self._check_channel_type(command_data.get("channel_type")):
            return

        if self.channel_type != "private" and not await self._get_user_permission(
            command_data.get("command_permission")
        ):
            return

        if "--help" in self.params:
            help_command = COMMANDS.get("details")
            if help_command and (help_function := help_command.get("func")):
                return await help_function(
                    self.message, self.command, command_data=command_data
                )

        if command_function := command_data.get("func"):
            return await command_function(self.message, self.params)
