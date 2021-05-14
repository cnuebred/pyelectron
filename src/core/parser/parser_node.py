from ...commands import *
from ...settings import PREFIX
from ...utils import is_member
from ..database.mongo_controller import Controller_mongo


class Command_Parser:
    def __init__(self, message) -> None:
        content_array = message.content.strip().split()
        self.message = message
        self.command = content_array[0][len(PREFIX) :]
        self.params = content_array[0:]
        self.channel_type = str(message.channel.type)
        self.guild = message.guild or None

    def _check_custom_command(self, all_permission):
        role_permission = Controller_mongo(_collection="guild").load(
            _filter={"guild_id": str(self.guild.id)},
            _folder="configuration.roles_commands",
        )
        for permissions in all_permission:
            if allow_commands := role_permission.get(permissions):
                if self.command in allow_commands:
                    return True

        return False

    def _compare_permissions(self, target_permission, all_permission=None):
        top_permission = all_permission[-1]
        if target_permission == "user" or top_permission == "root":
            return True
        elif target_permission == "custom" and all_permission:
            return self._check_custom_command(all_permission)
        elif target_permission == top_permission:
            return True

        return False

    async def _get_user_permission(self, target_permission):
        member = await is_member(self.message.author, self.guild)

        if not member:
            raise ("Member not found")

        message_author_permission = [str(role.id) for role in member.roles]

        command_permission = Controller_mongo(_collection="guild").load(
            _filter={"guild_id": str(self.guild.id)}, _folder="configuration.roles"
        )

        shared_permissions = [
            permission
            for permission in list(command_permission.values())
            if permission in message_author_permission
        ]

        if not shared_permissions:
            all_permission = ["user"]
        else:
            all_permission = [
                list(command_permission.keys())[
                    list(command_permission.values()).index(shared)
                ]
                for shared in shared_permissions
            ]

        return self._compare_permissions(target_permission, all_permission)

    def _check_channel_type(self, target_channel):
        if target_channel in ["text", "news"]:
            target_channel = "guild"

        if target_channel == "all":
            return True
        if target_channel == self.channel_type:
            return True

        return False

    async def parser(self):

        command_data = Controller_mongo(_collection="config").load(
            _filter={"category": "commands"}, _folder=f"commands.{self.command}"
        )

        if not command_data:
            return

        if not self._check_channel_type(command_data.get("channel_type")):
            return

        if "--help" in self.params:
            return await COMMANDS.get("details")(
                self.message, self.command, command_data
            )

        if self.channel_type != "private":
            if not await self._get_user_permission(command_data.get("permission")):
                return

        if self.command in list(COMMANDS.keys()):
            return await COMMANDS.get(self.command)(self.message, self.params)
