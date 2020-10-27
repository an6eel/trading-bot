from .worker import celery_app
from prediction.lstm import train_model
import asyncio


@celery_app.task
def celery_train_model(*args):
    asyncio.run(train_model(*args))
