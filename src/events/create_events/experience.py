import math

from discord.embeds import Embed

from ...core.database.postgres_controller import ControllerPostgres


class LevelSystem:
    def __init__(self) -> None:
        self.user_table: ControllerPostgres
        self.condition: str = ""

    def create_record(self, message):
        self.user_table.insert(
            values=[str(message.guild.id), str(message.author.id), 1, 1, 1]
        )

    def add_message_record(self, messages):
        messages += 1
        self.user_table.update(
            columns=["messages"], values=[messages], condition=self.condition
        )

    def level_algorithm(lvl):
        return math.floor(5 * lvl + (lvl * (lvl * 2 + lvl ** 2)) * 3) // int(
            (math.log2(lvl) * math.sqrt(lvl * lvl)) + 1
        )

    async def next_level(self, next_lvl, experience_sub, message):
        self.user_table.update(
            columns=["experience_user", "level_user"],
            values=[experience_sub, next_lvl],
            condition=self.condition,
        )
        embed_message = Embed(
            description=f"Gratuluję następnego poziomu ;)\n level ->**⁝ {next_lvl} ⁝**\n<@{message.author.id}>"
        )
        await message.channel.send(embed=embed_message)

    async def add_experience(self, message):
        self.user_table = ControllerPostgres("user_profile")
        self.condition = (
            f"user_id = '{message.author.id}' AND guild_id = '{message.guild.id}'"
        )

        exp_info = self.user_table.load(
            condition=self.condition,
        )

        if not exp_info:
            self.create_record(message)
            return

        exp_info = exp_info[0]

        self.add_message_record(exp_info["messages"])

        if len(message.content) < 5:
            return

        experience = exp_info["experience_user"] + 1 + len(message.content) // 100

        next_lvl_points = exp_info["level_user"] + 1

        points_to_next_lvl = self.level_algorithm(next_lvl_points)

        if experience > points_to_next_lvl:
            await self.next_level(
                next_lvl_points, (experience - points_to_next_lvl), message
            )
            return

        self.user_table.update(
            columns=["experience_user"], values=[experience], condition=self.condition
        )
