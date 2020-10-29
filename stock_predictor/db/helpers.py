import motor.motor_asyncio

from core.config import MONGO_PORT, MONGO_URL, TRAIN_TYPE
from models.stock_model import TrainingType
from db.db import db
from crud.symbol import generate_all_symbols


async def connect_to_mongo():
    db.client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://{}:{}'.format(MONGO_URL, MONGO_PORT))
    stocks_db = db.client["stocks"]
    collections = await stocks_db.list_collection_names()

    if TRAIN_TYPE == TrainingType.DAILY:
        if "symbols" not in collections:
            await stocks_db.create_collection("symbols")

        if "models" not in collections:
            await stocks_db.create_collection("models")
        db.symbols_collection = db.client["stocks"]["symbols"]
        db.stocks_collection = db.client["stocks"]["models"]
        await generate_all_symbols(db)
    else:
        db.symbols_collection = db.client["stocks"]["symbols"]
        db.stocks_collection = db.client["stocks"]["models"]


async def close_mongo():
    print("Connection lost")
    db.client.close()

