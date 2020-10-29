from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.helpers import close_mongo, connect_to_mongo
from routers.stocks import router as stock_router
from routers.models import router as models_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo)

app.include_router(stock_router, prefix="/stocks", tags=["stocks"])
app.include_router(models_router, prefix="/ml", tags=["models"])



