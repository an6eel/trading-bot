from datetime import datetime
import pandas_datareader.data as web


def yahoo_stocks(symbol, start, end):
    return web.DataReader(symbol, 'yahoo', start, end)


def get_stocks_data(symbol):
    return yahoo_stocks(symbol, datetime(2000, 1, 1), datetime.today())


def get_symbols():
    return {
        'Apple, Inc.': 'AAPL',
        'Alphabet, Inc.': 'GOOGL',
        'Microsoft Corp.': 'MSFT',
        'Tesla, Inc.': 'TSLA',
        'Twitter, Inc.': 'TWTR',
        'Amazon.com, Inc.': 'AMZN',
        'Advanced Micro Devices, Inc.': 'AMD',
        'Facebook, Inc.': 'FB',
        'Netflix, Inc.': 'NFLX',
        'NVIDIA Corp.': 'NVDA'
    }


