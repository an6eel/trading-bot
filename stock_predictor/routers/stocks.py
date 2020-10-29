from fastapi import APIRouter, Path, Depends, HTTPException
from db.db import get_database, DataBase
from controllers.stock_models import get_model_data
from crud.symbol import get_symbols
from models.symbol_model import SymbolItem

router = APIRouter()


@router.get('/{symbol}/data')
async def get_symbol_data(symbol: SymbolItem = Path(..., title="Symbol"), db: DataBase = Depends(get_database)):
    try:
        data = await get_model_data(db.stocks_collection, symbol)
        return data
    except:
        raise HTTPException(status_code=500, detail="Server error")


@router.get('/')
async def get_symbols_list(db: DataBase = Depends(get_database)):
    try:
        symbols = await get_symbols(db.symbols_collection)
        return symbols
    except:
        raise HTTPException(status_code=500, detail="Server error")
