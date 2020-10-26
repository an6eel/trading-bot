from fastapi import APIRouter, Request, Path, Depends, BackgroundTasks
import asyncio
from models.symbol import SymbolItem
from models.stock_model import TrainingStatus
from db.db import DataBase, get_database
from sse_starlette.sse import EventSourceResponse
from controllers.stock_models import get_model_status, get_model_predictions

import logging
from worker.worker import celery_app

router = APIRouter()


def celery_on_message(body):
    logging.info(body)


def background_on_message(task):
    logging.info(task.get(on_message=celery_on_message, propagate=False))


async def sse_train_model(
        request: Request,
        symbol: SymbolItem,
        db_client: DataBase,
        background_tasks: BackgroundTasks
):
    status = await get_model_status(db_client.stocks_collection, symbol)
    logging.info(status)
    if status == TrainingStatus.NOT_TRAINED:
        task = celery_app.send_task("prediction.lstm.train_model", args=[symbol])
        logging.info(task)
        background_tasks.add_task(background_on_message, task)
    while status != TrainingStatus.TRAINED:
        if await request.is_disconnected():
            break

        status = await get_model_status(db_client.stocks_collection, symbol)

        yield {
            "event": "status",
            "data": str(status)
        }

        await asyncio.sleep(5)

    yield {
        "event": "end",
    }


@router.get('/{symbol}/train')
async def train_symbol_model(
        request: Request,
        background_tasks: BackgroundTasks,
        symbol: SymbolItem = Path(..., title="Symbol"),
        db: DataBase = Depends(get_database)
):
    event_generator = sse_train_model(request, symbol, db, background_tasks)
    return EventSourceResponse(event_generator)


@router.get('/{symbol}/predictions')
async def get_symbol_predictions(
        symbol: SymbolItem = Path(..., title="Symbol"),
        db: DataBase = Depends(get_database))\
:
    predictions = await get_model_predictions(db.stocks_collection, symbol)
    return predictions
