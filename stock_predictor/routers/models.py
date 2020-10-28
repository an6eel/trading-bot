from fastapi import APIRouter, Request, Path, Depends, BackgroundTasks
import asyncio
from models.symbol_model import SymbolItem
from models.stock_model import TrainingStatus
from db.db import DataBase, get_database
from sse_starlette.sse import EventSourceResponse
from controllers.stock_models import get_model_status, get_model_predictions, get_model, update_model_status

import logging
from worker.tasks import celery_train_model
router = APIRouter()


async def sse_train_model(
        request: Request,
        symbol: SymbolItem,
        db_client: DataBase,
):
    status = await get_model_status(db_client.stocks_collection, symbol)
    model = await get_model(db_client.stocks_collection, symbol)
    logging.info(status)
    if status == TrainingStatus.NOT_TRAINED:
        task = celery_train_model.delay(model.dict())
    while True:
        if await request.is_disconnected():
            break
        elif status == TrainingStatus.TRAINED:
            yield {
                "event": "end",
                "data": "trained"
            }
            break

        task_state = task.state
        task_status = task.status
        state = await get_model_status(db_client.stocks_collection, symbol)

        if task_state == "START_TRAINING" or (state == TrainingStatus.NOT_TRAINED and task_status == 'PENDING'):
            await update_model_status(db_client.stocks_collection, symbol, TrainingStatus.TRAINING)
            yield {
                "event": "status",
                "data": "Train starting: {}".format(state)
            }
        elif task_state == "TRAINING_FAILED" or task_status == 'FAILURE':
            await update_model_status(db_client.stocks_collection, symbol, TrainingStatus.NOT_TRAINED)
            yield {
                "event": "end",
                "data": "failed"
            }
            break
        elif task_state == "TRAINING":
            progress = task.info.get("progress")
            if progress == 100:
                await update_model_status(db_client.stocks_collection, symbol, TrainingStatus.TRAINED)
                yield {
                    "event": "end",
                    "data": "trained"
                }
                break
            else:
                yield {
                    "event": "status",
                    "data": str(progress)
                }
        elif task_status == "SUCCESS":
            await update_model_status(db_client.stocks_collection, symbol, TrainingStatus.TRAINED)
            yield {
                "event": "end",
                "data": "trained"
            }
            break

        await asyncio.sleep(5)


@router.get('/{symbol}/train')
async def train_symbol_model(
        request: Request,
        symbol: SymbolItem = Path(..., title="Symbol"),
        db: DataBase = Depends(get_database)
):
    event_generator = sse_train_model(request, symbol, db)
    return EventSourceResponse(event_generator)


@router.get('/{symbol}/predictions')
async def get_symbol_predictions(
        symbol: SymbolItem = Path(..., title="Symbol"),
        db: DataBase = Depends(get_database))\
:
    predictions = await get_model_predictions(db.stocks_collection, symbol)
    return predictions
