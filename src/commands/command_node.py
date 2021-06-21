from ..core.database.postgres_controller import ControllerPostgres
from ..core.mockdata import COMMANDS

command_config = ControllerPostgres("config_commands")


def command_exe(func):
    name = func
    if not isinstance(func, str):
        name = func.__name__
        COMMANDS[name] = {"func": func}

    command_data = command_config.load(condition=f"command_name='{name}'")
    if command_data:
        command_data = command_data[0]
    else:
        command_data = {}

    COMMANDS[name]["command_permission"] = command_data.get("command_permission")
    COMMANDS[name]["channel_type"] = command_data.get("command_channel_type")
