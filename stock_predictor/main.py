from fastapi import FastAPI, Path, Query
from models.symbols import Symbol
from utils import get_historic_data
from prediction.lstm import train_model, get_predictions
app = FastAPI()


@app.get('/{symbol}/data')
def get_data(symbol: Symbol = Path(..., title="Symbol")):
    data = get_historic_data(symbol)
    return data


@app.post('/{symbol}/train')
def train_symbol_model(symbol: Symbol = Path(..., title="Symbol")):
    trained = train_model(symbol)
    return trained


@app.get('/{symbol}/predictions')
def get_symbol_predictions(symbol: Symbol = Path(..., title="Symbol")):
    predictions = get_predictions(symbol)
    return predictions
