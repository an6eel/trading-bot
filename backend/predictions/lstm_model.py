import numpy as np
import pandas as pd
from typing import Tuple
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from pathlib import Path
from datetime import timedelta

from keras.models import Model
from stocks import get_stocks_data
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import os
from datetime import datetime

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


def train_model(symbol: str, look_back: int, forward_days: int):
    model_path = Path("models", "{}-LB-{}-FD-{}-model.h5".format(symbol, look_back, forward_days))
    if model_path.exists():
        return {'trained': True}
    else:
        data = get_stocks_data(symbol)
        df = data['Close']
        array = df.values.reshape(df.shape[0], 1)
        scl = MinMaxScaler()
        array = scl.fit_transform(array)

        x, y = process_data(array, look_back, forward_days)
        y = np.array([list(a.ravel()) for a in y])
        x_train, x_validate, y_train, y_validate = train_test_split(x, y, test_size=0.20, random_state=42)

        model = build_model(look_back, forward_days)

        check_pointer = ModelCheckpoint(filepath=str(model_path),
                                        verbose=1,
                                        monitor='val_loss',
                                        mode='min',
                                        save_best_only=True)

        early_stopping = EarlyStopping(monitor='val_loss',
                                       patience=5,
                                       restore_best_weights=True)

        model.fit(x_train,
                  y_train,
                  epochs=100,
                  validation_data=(x_validate, y_validate),
                  shuffle=True,
                  batch_size=128,
                  verbose=2,
                  callbacks=(check_pointer, early_stopping)
                  )
        return {'trained': True}


def get_predictions(symbol: str, look_back: int, forward_days: int):
    model_path = Path("models", "{}-LB-{}-FD-{}-model.h5".format(symbol, look_back, forward_days))
    model: Model = load_model(model_path)

    data: pd.Series = get_stocks_data(symbol)

    data: pd.Series = data['Close']
    array: np.ndarray = data.values.reshape(data.shape[0], 1)
    scl: MinMaxScaler = MinMaxScaler()
    array: np.ndarray = scl.fit_transform(array)
    x_test, _ = process_data(array, look_back, forward_days)

    y_pred: np.ndarray = model.predict(np.expand_dims(x_test[-1], axis=0))

    predictions = scl.inverse_transform(y_pred.reshape(1, -1)).squeeze()

    response = {}

    date: datetime = pd.to_datetime(data.index[-1]) + timedelta(days=1)

    for forecast in predictions:
        response[date.isoformat()] = float(forecast)
        date += timedelta(days=1)

    return response
