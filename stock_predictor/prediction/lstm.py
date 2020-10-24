import numpy as np
import pandas as pd
from typing import Tuple
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from pathlib import Path
from datetime import timedelta

from keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import os
from config import TRAIN_TYPE
from models.training import TrainingType
from utils import get_historic_data
from typing import Dict
from utils import get_date_format
from datetime import datetime
from prediction.ws_callback import WebsocketCallback

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def process_data(data: np.ndarray, look_back: int, forward_days: int, jump: int = 1) -> Tuple[np.ndarray, np.ndarray]:
    X, Y = [], []
    for i in range(0, len(data) - look_back - forward_days + 1, jump):
        X.append(data[i:(i + look_back)])
        Y.append(data[(i + look_back):(i + look_back + forward_days)])
    return np.array(X), np.array(Y)


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


def get_look_back_time():
    if TRAIN_TYPE == TrainingType.DAILY:
        return 90
    elif TRAIN_TYPE == TrainingType.HOURLY:
        return 48
    else:
        return 240


def get_forward_day_time():
    if TRAIN_TYPE == TrainingType.DAILY:
        return 30
    elif TRAIN_TYPE == TrainingType.HOURLY:
        return 12
    else:
        return 60


def get_parsed_data(symbol: str):
    data: Dict = get_historic_data(symbol)['data']
    dates = data.keys()
    closes = data.values()
    df = pd.DataFrame(closes, index=dates, columns=['Close'])
    return df


def train_model(symbol: str):
    model_file = "{}-{}-model.h5".format(symbol, TRAIN_TYPE)
    model_path = Path("data", model_file)
    if model_path.exists():
        return True
    try:
        look_back = get_look_back_time()
        forward_days = get_forward_day_time()
        df = get_parsed_data(symbol)
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

        printer = WebsocketCallback(progress_callback=lambda progress: print("Progress", progress), end_callback=lambda: print("End"))

        model.fit(x_train,
                  y_train,
                  epochs=100,
                  validation_data=(x_validate, y_validate),
                  shuffle=True,
                  batch_size=128,
                  verbose=2,
                  callbacks=(check_pointer, early_stopping, printer)
                  )
        return True
    except Exception as e:
        print(e)
        return False



def predictions_offset():
    if TRAIN_TYPE == TrainingType.DAILY:
        return {'days': 1}
    elif TRAIN_TYPE == TrainingType.HOURLY:
        return {'hours': 1}
    else:
        return {'minutes': 1}


def get_predictions(symbol: str):
    model: Model = load_model("data/{}-{}-model.h5".format(symbol, TRAIN_TYPE))

    data = get_parsed_data(symbol)
    array: np.ndarray = data.values.reshape(data.shape[0], 1)
    scl: MinMaxScaler = MinMaxScaler()
    array: np.ndarray = scl.fit_transform(array)
    x_test, _ = process_data(array, get_look_back_time(), get_forward_day_time())

    y_pred: np.ndarray = model.predict(np.expand_dims(x_test[-1], axis=0))

    predictions = scl.inverse_transform(y_pred.reshape(1, -1)).squeeze()

    response = []

    date: datetime = pd.to_datetime(data.index[-1]) + timedelta(**predictions_offset())

    for forecast in predictions:
        response.append(
            {
                'date': date.strftime(get_date_format()),
                'value': float(forecast)
            }
        )
        date += timedelta(**predictions_offset())

    return response
