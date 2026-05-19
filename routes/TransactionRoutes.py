from fastapi import APIRouter
from datetime import datetime
from services.selectQuerys import ActiveStoreQuery
from services.selectQuerys import LimitValue
from services.insertQuerys import InsertTransaction
from models.TransactionStatusEnum import StatusEnum
from models.RiskEnum import RiskEnum
from decimal import Decimal
from fastapi import APIRouter, HTTPException

from schemas.requestDTOs.TransactionDTO import TransactionDTO

transaction_router = APIRouter(prefix="/transaction",tags="Transaction routes")

@transaction_router.post("/insert")
async def insertTransaction(payload: TransactionDTO):

    if not ActiveStoreQuery.ActiveStore(payload.storeID):
        message = ' Estabelecimento inativo.'
        status = StatusEnum.REJECTED
        risk = RiskEnum.HIGH

    elif (payload.value>LimitValue.StoreLimitQuery.storeLimit(payload.storeID)):
        message = ' Limite do estabelecimento excedido.'
        status = StatusEnum.REJECTED
        risk = RiskEnum.HIGH

    elif 6 > datetime.now().hour > 23 and payload.value> Decimal('200.00'):
        message = 'Limite noturno excedido.'
        status = StatusEnum.REJECTED
        risk = RiskEnum.HIGH

    elif payload.value <= Decimal('2.00'):
        message = 'Transação suspeita: valor abaixo do piso mínimo de segurança.'
        status = StatusEnum.PENDING
        risk = RiskEnum.MEDIUM

    payload.status = status
    payload.reason = message
    
    dbResponse = insertTransaction(payload)
    if dbResponse == "Erro no banco de dados":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="O motor antifraude falhou ao salvar a operação devido a uma instabilidade no banco de dados."
        )
    
    
    
