from db.db import DataBase, AsyncIOMotorCollection
from models.symbol_model import SymbolCreate, SymbolDB, SymbolItem, Symbol
from models.stock_model import StockModelCreate
from crud.stock_model import create_model
from bson import ObjectId
from core.utils import get_historic_data
from core.config import TRAIN_TYPE


async def create_symbol(db: DataBase, symbol: SymbolCreate) -> SymbolDB:
    db_symbol = SymbolDB(**symbol.dict())

    result = await db.symbols_collection.insert_one(db_symbol.dict())

    historic_data = get_historic_data(db_symbol.symbol_name)

    await create_model(db.stocks_collection, StockModelCreate(
        symbol=db_symbol.symbol_name,
        data=historic_data,
        path="data/{}-{}-model.h5".format(db_symbol.symbol_name, TRAIN_TYPE)
    ))
    db_symbol.id = str(result.inserted_id)
    db_symbol.updated_at = ObjectId(db_symbol.id).generation_time
    db_symbol.created_at = ObjectId(db_symbol.id).generation_time

    return db_symbol


async def get_symbol(db: AsyncIOMotorCollection, symbol: SymbolItem) -> SymbolDB:
    symbol_doc = await db.find_one({"symbol_name": symbol})
    if symbol_doc:
        return SymbolDB(**symbol_doc)


async def get_symbol_by_name(db: AsyncIOMotorCollection, name: str) -> SymbolDB:
    symbol_doc = await db.find_one({"name": name})
    if symbol_doc:
        return SymbolDB(**symbol_doc)


async def get_symbols(db_client: AsyncIOMotorCollection):
    symbols = []
    async for model in db_client.find():
        model_doc = Symbol(**model)
        model_doc.created_at = ObjectId(model["_id"]).generation_time
        symbols.append(model_doc)
    return symbols


async def generate_all_symbols(db_client: DataBase):
    count = await db_client.symbols_collection.estimated_document_count()
    if len(SymbolItem) != count:
        for symbol in SymbolItem:


            await create_symbol(db_client, SymbolCreate(symbol_name=symbol.value, name=symbol.name))
