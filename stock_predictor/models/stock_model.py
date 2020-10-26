from typing import Dict
from datetime import datetime
from enum import Enum
from models.rw_model import RWModel
from models.db_model import DBModelMixin, DateTimeModelMixin
from models.symbol_model import SymbolItem
import os


class TrainingType(str, Enum):
    HOURLY = "histohour"
    DAILY = "histoday"
    MINUTE = "histominute"


TRAIN_TYPE = os.getenv('TRAIN_TYPE', TrainingType.DAILY)


class TrainingStatus(str, Enum):
    NOT_TRAINED = "not_trained"
    TRAINING = "training"
    TRAINED = "trained"


class StockModelBase(RWModel):
    symbol: SymbolItem
    data: Dict[str, float]
    path: str


class StockModel(StockModelBase, DateTimeModelMixin):
    type: TrainingType = TRAIN_TYPE
    status: TrainingStatus = TrainingStatus.NOT_TRAINED
    predictions: Dict[str, float] = {}


class StockModelCreate(StockModelBase):
    pass


class StockModelDB(DBModelMixin, StockModel):
    pass


class StockModelUpdate(RWModel):
    data: Dict[datetime, float] = None
    status: TrainingStatus = None
    predictions: Dict[datetime, float] = None





