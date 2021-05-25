import discord

from src.events.event_node import event_node
from src.settings import TOKEN

bot = discord.Client()

# setup connection for mongo db

event_node(bot)

bot.run(TOKEN)
