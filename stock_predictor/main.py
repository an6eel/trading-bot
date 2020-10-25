from fastapi import BackgroundTasks, FastAPI, Path, Request, Depends
from models.symbols import Symbol
from prediction.lstm import train_model, get_predictions, AsyncTrainer
from sse_starlette.sse import EventSourceResponse
import asyncio
from concurrent.futures import ProcessPoolExecutor
from fastapi.middleware.cors import CORSMiddleware
from db.helpers import close_mongo, connect_to_mongo
from db.db import AsyncIOMotorClient, get_database
from models.Symbol import get_historic_data, get_model
from models.StockModel import StockModelOnDB, get_training_status, TrainingStatus, update_model_status
import logging
import functools
import concurrent.futures
import threading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def sse_train_model(
        request: Request,
        model: StockModelOnDB,
        db_client: AsyncIOMotorClient
):
    status = await get_training_status(db_client, str(model.id))
    await update_model_status(db_client, str(model.id), TrainingStatus.NOT_TRAINED)
    logging.info(status)
    if status == TrainingStatus.NOT_TRAINED.value:
        logging.info("Starting training")
        asyncio.create_task(train_model(model, db_client))
        # loop = asyncio.get_event_loop()
        # thread = threading.Thread(target=train_model, args=[model, db_client])
        # thread.start()
    while status != TrainingStatus.TRAINED:
        if await request.is_disconnected():
            break

        status = await get_training_status(db_client, str(model.id))
        logging.info("Progress: {}".format(status))

        yield {
            "event": "status",
            "data": status
        }

        await asyncio.sleep(5)
        
    yield {
        "event": "end",
    }


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo)


@app.get('/{symbol}/data')
async def get_data(symbol: Symbol = Path(..., title="Symbol"), db_client: AsyncIOMotorClient = Depends(get_database)):
    data = await get_historic_data(db_client, symbol)
    return data


@app.get('/{symbol}/train')
async def train_symbol_model(
        request: Request,
        background_tasks: BackgroundTasks,
        symbol: Symbol = Path(..., title="Symbol"),
        db_client: AsyncIOMotorClient = Depends(get_database)
):
    model: StockModelOnDB = await get_model(db_client, symbol)
    # logging.info(model)
    # background_tasks.add_task(async_train_model, model, db_client)
    event_generator = sse_train_model(request, model, db_client)
    return EventSourceResponse(event_generator)


@app.get('/{symbol}/predictions')
def get_symbol_predictions(symbol: Symbol = Path(..., title="Symbol")):
    predictions = get_predictions(symbol)
    return predictions
