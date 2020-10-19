from fastapi import FastAPI, Path, Query
from predictions.lstm_model import train_model, get_predictions
from stocks import get_stocks_data
from predictions.prophet import get_predictions_prophet

app = FastAPI()

# TODO This will be the model for the data stored in the db, to avoid sending
#     the same data for the train and predictions endpoints
#     class ModelParams(BaseModel):
#         path: str
#         forward_days: int
#         symbol: str
#         look_back: int


@app.get('/stocks/{symbol}')
def get_stocks(symbol: str = Path(..., title="Symbol name")):
    data = get_stocks(symbol)
    return data


@app.post('/stocks/{symbol}/train')
def train_symbol_model(
        symbol: str = Path(..., title="Symbol name"),
        look_back: int = Query(..., title="Look back model parameter"),
        forward_days: int = Query(..., title="Forward days model parameter"),
        epochs: int = Query(..., title="Epochs model parameter"),
):
    """
        TODO train task should run in queue to make a quick response
            We can make this endpoint as an websocket, and add a callback
            to the model to send the training process
    """
    train_model(symbol, look_back, forward_days, epochs, Path('models'))
    return {'message': 'Model saved. Predictions will be available for the next 20 days '}


@app.get('/stocks/{symbol}/predictions')
def get_symbol_predictions(
        symbol: str = Path(..., title="Symbol name"),
        look_back: int = Query(..., title="Look back model parameter"),
        forward_days: int = Query(..., title="Forward days model parameter")
):
    predictions = get_predictions(symbol, look_back, forward_days)
    print(predictions)
    return predictions


@app.get('/stocks/{symbol}/predictions_prophet')
async def get_symbol_predictions(
        symbol: str = Path(..., title="Symbol name"),
        forward_days: int = Query(..., title="Forward days model parameter")
):
    data = get_stocks_data(symbol)
    predictions = get_predictions_prophet(data, forward_days)
    return predictions
