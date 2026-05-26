from fastapi import FastAPI
import os,dotenv


dotenv.load_dotenv()

app = FastAPI()

from routes.TransactionRoutes import transaction_router

app.include_router(transaction_router)