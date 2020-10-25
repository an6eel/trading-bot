from fastapi import APIRouter, Path, Query
from predictions.lstm_model import train_model, get_predictions
from stocks import get_stocks_data, get_symbols

router = APIRouter()


@router.get('/stocks/{symbol}')
def get_stocks(symbol: str = Path(..., title="Symbol name")):
    data = get_stocks_data(symbol)
    return data['Close']


@router.post('/stocks/{symbol}/train')
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


@router.get('/stocks/{symbol}/predictions')
def get_symbol_predictions(
        symbol: str = Path(..., title="Symbol name"),
        look_back: int = Query(..., title="Look back model parameter"),
        forward_days: int = Query(..., title="Forward days model parameter")
):
    predictions = get_predictions(symbol, look_back, forward_days)
    return predictions


@router.get('/stocks')
def get_symbols_list():
    symbols = get_symbols
    return symbols
