import fastapi
from fastapi import FastAPI
import os,dotenv



dotenv.load_dotenv()

app = fastapi.FastAPI()

from routes.TransactionRoutes import transaction_router
from routes.StoreAndOwnersRoutes import store_and_owner_router
app.include_router(transaction_router)
app.include_router(store_and_owner_router)