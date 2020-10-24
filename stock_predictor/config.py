import os
from models.training import TrainingType

TRAIN_TYPE = os.getenv('TRAIN_TYPE', TrainingType.DAILY)
API_KEY = os.getenv('API_KEY')
API_BASE_URL = "https://min-api.cryptocompare.com/data/v2/"
