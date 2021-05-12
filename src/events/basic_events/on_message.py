from src.core.database.mongo_controller import Controller_mongo


async def on_message_node(message):
    category = Controller_mongo().load(_filter={"category": "new_data"})
    print(category)
    print(message.content)
