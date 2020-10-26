from models.stock_model import StockModelUpdate, StockModelDB, StockModelCreate, TrainingStatus
from models.symbol_model import SymbolItem
from db.db import AsyncIOMotorCollection
from bson import ObjectId
from core.config import TRAIN_TYPE


async def create_model(db: AsyncIOMotorCollection, model: StockModelCreate) -> StockModelDB:
    model_doc = model.dict()
    model_doc['type'] = TRAIN_TYPE
    result = await db.insert_one(model_doc)
    return StockModelDB(
        **model_doc,
        created_at=ObjectId(result.inserted_id).generation_time,
        updated_at=ObjectId(result.inserted_id).generation_time,
        id=str(result.inserted_id)
    )


async def get_model(db: AsyncIOMotorCollection, symbol: SymbolItem) -> StockModelDB:
    model_doc = await db.find_one({"symbol": symbol, 'type': TRAIN_TYPE})

    create_prop = {'created_at': ObjectId(model_doc["_id"]).generation_time} if 'created_at' not in model_doc else {}
    id_prop = {'id': str(ObjectId(model_doc["_id"]))} if 'id' not in model_doc else {}

    if model_doc:
        return StockModelDB(
            **model_doc,
            **create_prop,
            **id_prop
        )


async def update_model(db: AsyncIOMotorCollection, symbol: SymbolItem, model_update: StockModelUpdate) -> StockModelDB:
    model: StockModelDB = await get_model(db, symbol)

    if model_update.status:
        model.status = model_update.status
    if model_update.predictions:
        model.predictions = model_update.predictions
    if model_update.data:
        model.data = model_update.data


    updated_at = await db.replace_one({"symbol": symbol, "type": TRAIN_TYPE}, model.dict())
    model.updated_at = updated_at
    return model


async def get_training_status(db: AsyncIOMotorCollection, symbol: SymbolItem) -> TrainingStatus:
    model_data = await get_model(db, symbol)
    return model_data.status
