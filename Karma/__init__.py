from os import environ, path, sys

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client

if path.exists("config.env"):
    load_dotenv("config.env")

REQUIRED_KEYS = ["API_ID", "API_HASH", "BOT_TOKEN", "DB_URI"]
for _key in REQUIRED_KEYS:
    if not environ.get(_key):
        print(f"{_key} is missing.")
        sys.exit(1)

# MongoDB client
print("[INFO]: INITIALIZING DATABASE")
mongo_client = MongoClient(environ["DB_URI"])
db = mongo_client.Karma


class Karma(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            name,
            api_id=environ["API_ID"],
            api_hash=environ["API_HASH"],
            bot_token=environ["BOT_TOKEN"],
            plugins=dict(root=f"{name.capitalize()}.plugins"),
        )
