from celery import Celery
from celery.utils.log import get_task_logger

LOGGER = get_task_logger(__name__)
APP_NAME = 'trainer'

celery_app = Celery(
        APP_NAME,
        backend="redis://:password123@redis:6379/0",
        broker="amqp://user:bitnami@rabbitmq:5672//"
    )
celery_app.conf.task_routes = {
    "app.prediction.lstm.train_model": "test-queue"
}