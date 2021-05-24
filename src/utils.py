async def is_member(user, guild):
    if not (isinstance(user, str) or isinstance(user, int)):
        return await guild.fetch_member(int(user.id))
    return await guild.fetch_member(int(user))
    # raise TypeError("User must by specyfied by str or int (id)")


TERMINAL_COLORS = {
    "H": "\033[95m",  # header
    "BL": "\033[94m",  # blue
    "C": "\033[96m",  # cyan
    "G": "\033[92m",  # green
    "W": "\033[93m",  # warning
    "F": "\033[91m",  # fail
    "E": "\033[0m",  # end
    "B": "\033[1m",  # bold
    "U": "\033[4m",  # underline
}


def log(*args):
    if not isinstance(args, tuple):
        args = tuple(args)
    for type, special_string in args:
        if isinstance(type, list):
            type = "".join(
                [TERMINAL_COLORS.get(type_color.upper()) for type_color in type]
            )
        else:
            type = TERMINAL_COLORS.get(type.upper())
        print(
            f"{type}{special_string}{TERMINAL_COLORS.get('E')}",
            end=" ",
        )
    print("\n")
