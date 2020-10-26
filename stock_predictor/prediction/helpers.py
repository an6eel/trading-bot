import pandas as pd
from core.config import TRAIN_TYPE
from models.stock_model import TrainingType
from typing import Dict, Tuple
import numpy as np
from datetime import datetime


def get_look_back_time():
    if TRAIN_TYPE == TrainingType.DAILY:
        return 120
    elif TRAIN_TYPE == TrainingType.HOURLY:
        return 96
    else:
        return 480


def get_forward_day_time():
    if TRAIN_TYPE == TrainingType.DAILY:
        return 30
    elif TRAIN_TYPE == TrainingType.HOURLY:
        return 12
    else:
        return 60


def get_parsed_data(data: Dict[datetime, float]):
    dates = data.keys()
    closes = data.values()
    df = pd.DataFrame(closes, index=dates, columns=['Close'])
    return df


def process_data(data: np.ndarray, look_back: int, forward_days: int, jump: int = 1) -> Tuple[np.ndarray, np.ndarray]:
    X, Y = [], []
    for i in range(0, len(data) - look_back - forward_days + 1, jump):
        X.append(data[i:(i + look_back)])
        Y.append(data[(i + look_back):(i + look_back + forward_days)])
    return np.array(X), np.array(Y)


def predictions_offset():
    if TRAIN_TYPE == TrainingType.DAILY:
        return {'days': 1}
    elif TRAIN_TYPE == TrainingType.HOURLY:
        return {'hours': 1}
    else:
        return {'minutes': 1}