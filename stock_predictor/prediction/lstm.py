import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from pathlib import Path
from datetime import timedelta

from keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from prediction.helpers import (
    predictions_offset,
    get_forward_day_time,
    get_look_back_time,
    get_parsed_data,
    process_data
)
from datetime import datetime
from models.stock_model import TrainingStatus
from models.symbol_model import SymbolItem
from controllers.stock_models import get_model, update_model_status, complete_training
from worker.worker import celery_app
from celery import current_task
from db.db import get_database, DataBase
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


def build_model(look_back: int, forward_days: int) -> Model:
    first_layer_neurons = 256
    second_layer_neurons = 128
    third_layer_neurons = 64
    forth_layer_neurons = 32

    model = Sequential()
    model.add(LSTM(first_layer_neurons, input_shape=(look_back, 1), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(second_layer_neurons, input_shape=(first_layer_neurons, 1), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(third_layer_neurons, input_shape=(second_layer_neurons, 1), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(forth_layer_neurons, input_shape=(third_layer_neurons, 1)))
    model.add(Dropout(0.2))
    model.add(Dense(forward_days))
    model.compile(loss='mean_squared_error', optimizer='adam')

    return model


@celery_app.task
async def train_model(symbol: SymbolItem):
    db: DataBase = get_database()
    db_client = db.stocks_collection
    stock_model = await get_model(db_client, symbol)
    logger.debug(stock_model)
    current_task.update_state(state="PROGRESS", meta={'progress_percent': 33})
    model_path = Path(stock_model.path)
    try:
        look_back = get_look_back_time()
        forward_days = get_forward_day_time()
        df = get_parsed_data(stock_model.data)
        array = df.values.reshape(df.shape[0], 1)

        scl = MinMaxScaler()
        array = scl.fit_transform(array)

        x, y = process_data(array, look_back, forward_days)
        y = np.array([list(a.ravel()) for a in y])
        x_train, x_validate, y_train, y_validate = train_test_split(x, y, test_size=0.20, random_state=42)

        model = build_model(look_back, forward_days)

        check_pointer = ModelCheckpoint(filepath=model_path,
                                        verbose=1,
                                        monitor='val_loss',
                                        mode='min',
                                        save_best_only=True)

        early_stopping = EarlyStopping(monitor='val_loss',
                                       patience=5,
                                       restore_best_weights=True)
        await update_model_status(db_client, symbol, TrainingStatus.TRAINING)
        logger.debug("training")
        current_task.update_state(state="PROGRESS", meta={'progress_percent': 53})
        model.fit(x_train,
                  y_train,
                  epochs=100,
                  validation_data=(x_validate, y_validate),
                  shuffle=True,
                  batch_size=128,
                  verbose=2,
                  callbacks=(check_pointer, early_stopping)
                  )
        predictions = get_predictions(df, model)

        await complete_training(db_client, symbol, predictions)
        return True
    except Exception as e:
        await update_model_status(db_client, symbol, TrainingStatus.NOT_TRAINED)
        return False


def get_predictions(df: pd.DataFrame, model: Model):
    array: np.ndarray = df.values.reshape(df.shape[0], 1)
    scl: MinMaxScaler = MinMaxScaler()
    array: np.ndarray = scl.fit_transform(array)
    x_test, _ = process_data(array, get_look_back_time(), get_forward_day_time())

    y_pred: np.ndarray = model.predict(np.expand_dims(x_test[-1], axis=0))

    predictions = scl.inverse_transform(y_pred.reshape(1, -1)).squeeze()

    response = {}

    date: datetime = pd.to_datetime(df.index[-1]) + timedelta(**predictions_offset())

    for forecast in predictions:
        response[date] = float(forecast)
        date += timedelta(**predictions_offset())

    return response
