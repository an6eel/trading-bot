from enum import Enum
from models.db_model import DateTimeModelMixin, DBModelMixin
from models.rw_model import RWModel


class SymbolItem(str, Enum):
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


class Symbol(RWModel, DateTimeModelMixin):
    symbol_name: SymbolItem
    name: str


class SymbolDB(DBModelMixin, Symbol):
    pass


class SymbolResponse(RWModel):
    symbol: Symbol


class SymbolCreate(Symbol):
    pass
