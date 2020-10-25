from typing import Optional
from pydantic import BaseModel, Field
from models.StockModel import StockModelOnDB, StockModelBase, create_model
from models.symbols import Symbol
from db.db import AsyncIOMotorClient
from config import DB_NAME, DB_SYMBOLS_COLLECTION
import logging

class SymbolModelBase(BaseModel):
    symbol_name: str = Field(...)
    name: str = Field(...)


class SymbolModel(SymbolModelBase):
    id: Optional[int] = None
    model: Optional[StockModelOnDB]


async def get_symbols(db_client: AsyncIOMotorClient):
    symbols = []
    async for model in db_client[DB_NAME][DB_SYMBOLS_COLLECTION].find():
        symbols.append(SymbolModelBase(**model))
    return symbols


async def get_symbol(db_client: AsyncIOMotorClient, symbol: str) -> SymbolModel:
    result = await db_client[DB_NAME][DB_SYMBOLS_COLLECTION].find_one({"symbol_name": symbol})
    symbol_result = SymbolModel(**result)
    return symbol_result


async def create_symbol(db_client: AsyncIOMotorClient, name: str, symbol: str):
    model: StockModelOnDB = await create_model(db_client, symbol)
    new_symbol_data = {
        'name': name,
        'symbol_name': symbol,
        'model': model
    }
    db_symbol = SymbolModel(**new_symbol_data)
    result = await db_client[DB_NAME][DB_SYMBOLS_COLLECTION].insert_one(db_symbol.dict())
    db_symbol.id = result.inserted_id
    return db_symbol


async def generate_all_symbols(db_client: AsyncIOMotorClient):
    count = await db_client[DB_NAME][DB_SYMBOLS_COLLECTION].estimated_document_count()
    if len(Symbol) != count:
        for symbol in Symbol:
            await create_symbol(db_client, symbol.name, symbol.value)


async def get_historic_data(db_client: AsyncIOMotorClient, symbol: str):
    symbol_data = await get_symbol(db_client, symbol)
    return symbol_data.model.data


async def get_symbol_predictions(db_client: AsyncIOMotorClient, symbol: str):
    symbol_data = await get_symbol(db_client, symbol)
    return symbol_data.model.predictions


async def check_symbol_training_status(db_client: AsyncIOMotorClient, symbol: str):
    symbol_data = await get_symbol(db_client, symbol)
    return symbol_data.model.trained, symbol_data.model.progress


async def get_model_id(db_client: AsyncIOMotorClient, symbol: str):
    symbol_data = await get_symbol(db_client, symbol)
    return symbol_data.model.id


async def get_model(db_client: AsyncIOMotorClient, symbol: str):
    symbol_data = await get_symbol(db_client, symbol)
    return symbol_data.model
