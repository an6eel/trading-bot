from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


class DataBase:
    client: AsyncIOMotorClient = None
    stocks_collection: AsyncIOMotorCollection = None
    symbols_collection: AsyncIOMotorCollection = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db
