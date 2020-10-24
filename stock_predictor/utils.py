import requests
from config import API_BASE_URL, TRAIN_TYPE, API_KEY
from models.symbols import Symbol
from models.training import TrainingType
from datetime import datetime
from pytz import timezone


def get_historic_data(symbol: Symbol):
    limit = 80 * 24 if TRAIN_TYPE == TrainingType.HOURLY else 24 * 60
    all_data = "&allData=true" if TRAIN_TYPE == TrainingType.DAILY else "&limit={}".format(limit)
    url = "{}{}?fsym={}&tsym=EUR{}&api_key={}".format(API_BASE_URL, TRAIN_TYPE, symbol, all_data, API_KEY)
    data = requests.get(url)
    return parse_data_response(data.json())


def get_date_format():
    if TRAIN_TYPE == TrainingType.DAILY:
        return "%Y-%m-%d"
    else:
        return "%Y-%m-%d %H:%M"


def parse_data_response(data_response):
    try:
        response = {}
        data = data_response['Data']
        response['TimeFrom'] = datetime.fromtimestamp(data['TimeFrom']).astimezone(timezone('Europe/Madrid'))
        response['TimeTo'] = datetime.fromtimestamp(data['TimeTo']).astimezone(timezone('Europe/Madrid'))
        response['data'] = {}
        stock_data = data['Data']
        for day in stock_data:
            close_value = day['close']
            date = datetime.fromtimestamp(day['time']).astimezone(timezone('Europe/Madrid')).strftime(get_date_format())
            response['data'][date] = close_value
        parse_data_response(response)
        return response
    except KeyError:
        return {}
