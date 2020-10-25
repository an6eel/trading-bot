from models.training import TrainingType
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from config import TRAIN_TYPE, DB_MODELS_COLLECTION, DB_NAME
from db.db import AsyncIOMotorClient
from models.symbols import Symbol
from utils import get_historic_data
from bson.objectid import ObjectId as BsonObjectId
from enum import Enum
import logging


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)


class TrainingStatus(Enum):
    NOT_TRAINED = "not_trained"
    TRAINING = "training"
    TRAINED = "trained"


class StockModelBase(BaseModel):
    type: TrainingType
    data: Dict[str, float]
    status: str
    path: str
    predictions: Dict[str, float]


class StockModelOnDB(StockModelBase):
    id: str


class StockModelUpdate(BaseModel):
    type: TrainingType = None
    data: Dict[str, float] = None
    status: str = None
    path: str = None
    predictions: Dict[str, float] = None


def get_default_model_data(symbol: str, data: Dict[datetime, float]):
    return {
        'type': TRAIN_TYPE,
        'data': data,
        'status': TrainingStatus.NOT_TRAINED.value,
        'path': str(Path('data', "{}-{}-model.h5".format(symbol, TRAIN_TYPE))),
        'predictions': {}
    }


def update_data_in_db(new_model: StockModelOnDB) :
    return {
        'type': new_model.type,
        'data': new_model.data,
        'status': new_model.status,
        'path': new_model.path,
        'predictions': new_model.predictions
    }


async def retrieve_models(db_client: AsyncIOMotorClient, model_type: Optional[TrainingType] = None) -> List[StockModelOnDB]:
    find_params = {'type': model_type} if model_type is not None else {}
    models = []
    async for model in db_client[DB_NAME][DB_MODELS_COLLECTION].find(**find_params):
        models.append(StockModelOnDB(**model, id=str(model['_id'])))
    return models


async def get_model_by_id(db_client: AsyncIOMotorClient, model_id: str):
    result = await db_client[DB_NAME][DB_MODELS_COLLECTION].find_one({"_id": BsonObjectId(model_id)})
    logging.info(result)
    return StockModelOnDB(**result, id=str(result['_id']))


async def create_model(db_client: AsyncIOMotorClient, symbol: Symbol):
    data = get_historic_data(symbol)
    db_model = StockModelBase(**get_default_model_data(symbol, data))
    result = await db_client[DB_NAME][DB_MODELS_COLLECTION].insert_one(db_model.dict())
    new_model = StockModelOnDB(**db_model.dict(), id=str(result.inserted_id))
    return new_model


async def update_model_status(db_client: AsyncIOMotorClient, model_id: str, status: TrainingStatus):
    model_data = await get_model_by_id(db_client, model_id)
    model_data.status = str(status.value)
    await db_client[DB_NAME][DB_MODELS_COLLECTION].update_one({"_id": model_id}, {'$set', update_data_in_db(model_data) })
    return model_data


async def update_predictions(db_client: AsyncIOMotorClient, model_id: str, predictions: Dict[str, float]):
    model_data = await get_model_by_id(db_client, model_id)
    model_data.predictions = predictions
    await db_client[DB_NAME][DB_MODELS_COLLECTION]\
        .update_one({"_id": BsonObjectId(model_id)}, {'$set', model_data.dict()})
    return model_data


async def update_model_data(db_client: AsyncIOMotorClient, model_id: str, symbol: Symbol):
    model_data = await get_model_by_id(db_client, model_id)
    new_data = get_historic_data(symbol)
    model_data.data = new_data
    model_path = Path(model_data.path)
    if model_path.exists():
        model_path.unlink()
    model_data.status = TrainingStatus.NOT_TRAINED
    await db_client[DB_NAME][DB_MODELS_COLLECTION].update_one({"_id": BsonObjectId(model_id)}, {'$set', model_data.dict()})
    return model_data


async def get_training_status(db_client: AsyncIOMotorClient, model_id: str) -> TrainingStatus:
    model_data = await get_model_by_id(db_client, model_id)
    return model_data.status



