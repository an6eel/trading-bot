from crud.stock_model import get_model, update_model
from db.db import AsyncIOMotorCollection
from models.symbol_model import SymbolItem
from models.stock_model import StockModelUpdate, TrainingStatus
from core.utils import get_historic_data
from datetime import datetime
from typing import Dict


async def get_model_status(db: AsyncIOMotorCollection, symbol: SymbolItem):
    model = await get_model(db, symbol)
    return model.status


async def update_model_status(db: AsyncIOMotorCollection, symbol: SymbolItem, new_status: TrainingStatus):
    update_data = StockModelUpdate(status=new_status)
    await update_model(db, symbol, update_data)
    

async def update_model_data(db: AsyncIOMotorCollection, symbol: SymbolItem):
    data = get_historic_data(symbol)
    update_data = StockModelUpdate(status=TrainingStatus.NOT_TRAINED, data=data, predictions={})
    await update_model(db, symbol, update_data)


async def get_model_data(db: AsyncIOMotorCollection, symbol: SymbolItem):
    model = await get_model(db, symbol)
    return model.data


async def get_model_predictions(db: AsyncIOMotorCollection, symbol: SymbolItem):
    model = await get_model(db, symbol)
    return model.predictions


async def complete_training(db: AsyncIOMotorCollection, symbol: SymbolItem, predictions: Dict[datetime, float]):
    update_data = StockModelUpdate(status=TrainingStatus.TRAINED, predictions=predictions)
    await update_model(db, symbol, update_data)

