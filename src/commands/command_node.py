from ..core.database.postgres_controller import ControllerPostgres
from ..core.mockdata import COMMANDS

command_config = ControllerPostgres("config_commands")


def command_exe(func):
    command_data = command_config.load(condition=f"command_name='{func.__name__}'")
    if command_data:
        command_data = command_data[0]
    else:
        command_data = {}

    COMMANDS[func.__name__] = {
        "func": func,
        "command_permission": command_data.get("command_permission"),
        "channel_type": command_data.get("command_channel_type"),
    }
