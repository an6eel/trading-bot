import os
from models.training import TrainingType

TRAIN_TYPE = os.getenv('TRAIN_TYPE', TrainingType.DAILY)
API_KEY = os.getenv('API_KEY')
API_BASE_URL = "https://min-api.cryptocompare.com/data/v2/"
MONGO_URL = os.getenv('MONGO_URL')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
DB_NAME = "stocks"
DB_SYMBOLS_COLLECTION = "symbols"
DB_MODELS_COLLECTION = "models"
