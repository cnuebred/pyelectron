from ..core.mockdata import COMMANDS


def command_exe(func):
    COMMANDS[func.__name__] = func
