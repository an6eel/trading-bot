from fastapi import APIRouter, Path, Depends
from db.db import get_database, DataBase
from controllers.stock_models import get_model_data
from crud.symbol import get_symbols
from models.symbol import SymbolItem

router = APIRouter()


@router.get('/{symbol}/data')
async def get_symbol_data(symbol: SymbolItem = Path(..., title="Symbol"), db: DataBase = Depends(get_database)):
    data = await get_model_data(db.stocks_collection, symbol)
    return data


@router.get('/')
async def get_symbols_list(db: DataBase = Depends(get_database)):
    symbols = await get_symbols(db.symbols_collection)
    return symbols

