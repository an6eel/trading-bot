import requests
from core.config import API_BASE_URL, TRAIN_TYPE, API_KEY
from models.symbol_model import SymbolItem
from models.stock_model import TrainingType
from datetime import datetime
from pytz import timezone


def get_historic_data(symbol: SymbolItem):

    limit = 80 * 24 if TRAIN_TYPE == TrainingType.HOURLY else 24 * 60
    all_data = "&allData=true" if TRAIN_TYPE == TrainingType.DAILY else "&limit={}".format(limit)
    url = "{}{}?fsym={}&tsym=EUR{}&api_key={}".format(API_BASE_URL, TRAIN_TYPE, symbol, all_data, API_KEY)
    data = requests.get(url)
    return parse_data_response(data.json())


def parse_data_response(data_response):
    try:
        data = data_response['Data']
        response = {}
        stock_data = data['Data']
        for day in stock_data:
            close_value = day['close']
            date = datetime.fromtimestamp(day['time']).astimezone(timezone('Europe/Madrid')).isoformat()
            response[date] = close_value
        return response
    except Exception as e:

        return {}
