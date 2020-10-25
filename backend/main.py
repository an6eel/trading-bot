from fastapi import FastAPI
from routers import agent, stocks

app = FastAPI()

app.include_router(agent.router, prefix='/api')
app.include_router(stocks.router, prefix='/api')
