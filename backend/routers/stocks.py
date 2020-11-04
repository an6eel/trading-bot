from fastapi import APIRouter, Path, Query, HTTPException
from predictions.lstm_model import train_model, get_predictions
from stocks import get_stocks_data, get_symbols
from starlette.status import HTTP_400_BAD_REQUEST
router = APIRouter()


@router.get('/stocks/{symbol}')
def get_stocks(symbol: str = Path(..., title="Symbol name")):
    try:
        data = get_stocks_data(symbol)
        return data['Close']
    except:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)


@router.post('/stocks/{symbol}/train')
def train_symbol_model(
        symbol: str = Path(..., title="Symbol name"),
        look_back: int = Query(..., title="Look back model parameter"),
        forward_days: int = Query(..., title="Forward days model parameter"),
):
    try:
        response = train_model(symbol, look_back, forward_days)
        return response
    except:
        return {'trained': False}


@router.get('/stocks/{symbol}/predictions')
def get_symbol_predictions(
        symbol: str = Path(..., title="Symbol name"),
        look_back: int = Query(..., title="Look back model parameter"),
        forward_days: int = Query(..., title="Forward days model parameter")
):
    try:
        predictions = get_predictions(symbol, look_back, forward_days)
        return predictions
    except:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)


@router.get('/stocks')
def get_symbols_list():
    try:
        symbols = get_symbols()
        return symbols
    except:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)
