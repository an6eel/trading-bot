from predictions.lstm_model import get_predictions
import pandas as pd
from stocks import get_stocks_data
import numpy as np


def get_best_actions(df_signal):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1
    for i in range(0, len(df_signal)):
        if df_signal['SMA7'][i] > df_signal['SMA30'][i]:
            if flag != 1:
                sigPriceBuy.append(df_signal['AAPL'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif df_signal['SMA7'][i] < df_signal['SMA30'][i]:
            if flag != 0:
                sigPriceSell.append(df_signal['AAPL'][i])
                sigPriceBuy.append(np.nan)
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return sigPriceBuy, sigPriceSell


def get_actions(symbol: str, look_back: int, forward_days: int):
    historic: pd.Series = get_stocks_data(symbol)['Close']
    predictions = get_predictions(symbol, look_back, forward_days)
    data = np.array(list(predictions.values()))
    historic_dates = np.array(historic.index.to_pydatetime(), dtype=np.datetime64)
    predictions_dates = np.array(list(predictions.keys()), dtype=np.datetime64)
    df_index = np.concatenate((historic_dates, predictions_dates))
    df_data = np.concatenate((historic.values, data))
    df = pd.DataFrame(df_data, columns=['AAPL'], index=df_index)

    SMA7 = df.rolling(window=7).mean()
    SMA30 = df.rolling(window=30).mean()

    signal = pd.DataFrame(index=df['AAPL'].index)
    signal['AAPL'] = df['AAPL']
    signal['SMA7'] = SMA7['AAPL']
    signal['SMA30'] = SMA30['AAPL']

    x = get_best_actions(signal)
    signal['Buy'] = x[0]
    signal['Sell'] = x[1]

    signal = signal[['Buy', 'Sell']]
    signal = signal[pd.notna(signal['Buy']) != pd.notna(signal['Sell'])]

    actions = {}
    for index, row in signal.iterrows():
        actions[index] = 'BUY' if pd.notna(row['Buy']) else 'SELL'

    return actions
