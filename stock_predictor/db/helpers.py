import motor.motor_asyncio

from config import MONGO_PORT, MONGO_URL
from db.db import db
from models.Symbol import generate_all_symbols


async def connect_to_mongo():
    db.client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://{}:{}'.format(MONGO_URL, MONGO_PORT))
    stocks_db = db.client["stocks"]
    collections = await stocks_db.list_collection_names()

    if "symbols" not in collections:
        await stocks_db.create_collection("symbols")

    if "models" not in collections:
        await stocks_db.create_collection("models")

    await generate_all_symbols(db.client)


async def close_mongo():
    print("Connection lost")
    db.client.close()

