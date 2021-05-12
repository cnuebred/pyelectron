import discord

from src.core.database.mongo_controller import Connection_mongo
from src.events.event_node import event_node
from src.settings import TOKEN

bot = discord.Client()

Connection_mongo().connect()
# setup connection for mongo db

event_node(bot)

bot.run(TOKEN)
