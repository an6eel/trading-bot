from enum import Enum


class Symbol(str, Enum):
    BITCOIN = 'BTC'
    ETHEREUM = 'ETH'
    LITECOIN = 'LTC'
    CHAINLINK = 'LINK'
    BITCOIN_CASH = 'BCH'
    XRP = 'XRP'
    EOS = 'EOS'
    TETHER = 'USDT'
    TRON = "TRX"
    BINANCE_COIN = 'BNB'