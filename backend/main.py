from fastapi import FastAPI, Path, Query
from predictions.lstm_model import train_model, get_predictions
from stocks import get_stocks_data, get_symbols
from agent import get_actions

app = FastAPI()


@app.get('/stocks/{symbol}')
def get_stocks(symbol: str = Path(..., title="Symbol name")):
    data = get_stocks_data(symbol)
    return data['Close']


@app.post('/stocks/{symbol}/train')
def train_symbol_model(
        symbol: str = Path(..., title="Symbol name"),
        look_back: int = Query(..., title="Look back model parameter"),
        forward_days: int = Query(..., title="Forward days model parameter"),
):
    try:
        response = train_model(symbol, look_back, forward_days, Path('models'))
        return response
    except:
        return {'trained': False}


@app.get('/stocks/{symbol}/predictions')
def get_symbol_predictions(
        symbol: str = Path(..., title="Symbol name"),
        look_back: int = Query(..., title="Look back model parameter"),
        forward_days: int = Query(..., title="Forward days model parameter")
):
    predictions = get_predictions(symbol, look_back, forward_days)
    print(predictions)
    return predictions


@app.get('/agent/{symbol}/actions')
def get_agent_actions(
        symbol: str = Path(..., title="Symbol name"),
        look_back: int = Query(..., title="Look back model parameter"),
        forward_days: int = Query(..., title="Forward days model parameter")):
    actions = get_actions(symbol, look_back, forward_days)
    return actions

@app.get('/symbols')
def get_symbols_list():
    symbols = get_symbols
    return symbols