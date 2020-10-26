from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from db.helpers import close_mongo, connect_to_mongo
from routers.stocks import router as stock_router
from routers.models import router as models_router
from core.config import TRAIN_TYPE

app = FastAPI()
base_router = APIRouter()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo)

base_router.include_router(stock_router, prefix="/stocks", tags=["stocks"])
base_router.include_router(models_router, prefix="/ml", tags=["models"])

app.include_router(base_router, prefix="/{}".format(TRAIN_TYPE))


