async def is_member(user, guild):
    if not (isinstance(user, str) or isinstance(user, int)):
        return await guild.fetch_member(int(user.id))
    else:
        return await guild.fetch_member(int(user))
        # raise TypeError("User must by specyfied by str or int (id)")
