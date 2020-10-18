from datetime import datetime
import pandas_datareader.data as web


def yahoo_stocks(symbol, start, end):
    return web.DataReader(symbol, 'yahoo', start, end)


def get_stocks_data(symbol):
    return yahoo_stocks(symbol, datetime(2000, 1, 1), datetime.today())

