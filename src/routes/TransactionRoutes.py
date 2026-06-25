from fastapi import APIRouter,HTTPException,status
from datetime import datetime
from src.services.selectQuerys.ActiveStoreQuery import ActiveStore
from src.services.selectQuerys.SelectLimitValue import StoreLimitQuery
from src.services.insertQuerys.InsertTransaction import InsertTransaction as it
from src.models.TransactionStatusEnum import StatusEnum
from src.services.selectQuerys.SelectStoreLocation import StoreLocation
from src.models.RiskEnum import RiskEnum
from src.services.calcHaversine import calcHaversine
from decimal import Decimal
from src.schemas.requestDTOs.TransactionDTO import TransactionDTO
from src.services.updateQuerys.TransactionStatus import AlterTransaction
from src.schemas.requestDTOs.TransactionStatusDTO import TransactionStatus
import os

transaction_router = APIRouter(prefix="/transaction",tags=['Transaction routes'])

@transaction_router.post("/insert")
def insertTransaction(payload: TransactionDTO):

    statusTransaction = StatusEnum.PENDING
    risk = RiskEnum.LOW
    message = ''
    
    if not ActiveStore(payload.storeID):
        message += '\n Estabelecimento inativo.'
        statusTransaction = StatusEnum.REJECTED
        risk = RiskEnum.HIGH

    elif payload.value>StoreLimitQuery.storeLimit(payload.storeID):
        message += '\n Limite do estabelecimento excedido.'
        statusTransaction = StatusEnum.PENDING
        risk = RiskEnum.HIGH

    elif (datetime.now().hour > 23 or datetime.now().hour < 6) and payload.value> Decimal('200.00'):
        message += '\n Limite noturno excedido.'
        statusTransaction = StatusEnum.PENDING
        risk = RiskEnum.HIGH

    elif payload.value <= Decimal('2.00'):
        message += '\n Transação suspeita: valor jabaixo do piso mínimo de segurança.'
        statusTransaction = StatusEnum.PENDING
        risk = RiskEnum.MEDIUM

    storeInfo = StoreLocation.GetLocation(payload.storeID)
    
    if storeInfo:
        dStoreTransaction = calcHaversine(payload.location[0],
                                          payload.location[1],
                                          storeInfo['lat'],
                                          storeInfo['lon'])
    
        if dStoreTransaction > storeInfo['fence_dis']:
            message += f'''Transação suspeita: cerca eletrônica violada,
            a compra foi feita a distância de {dStoreTransaction:.2f} metros do local da sede
            do estabelecimento
            '''
            statusTransaction = StatusEnum.PENDING
            risk = RiskEnum.HIGH
    else:
        message+="Erro na localização da transação."
        risk = RiskEnum.HIGH
        statusTransaction = StatusEnum.REJECTED
        

    payload.reason = message  
    payload.status = statusTransaction
    payload.risk = risk
   
    response = it.insertTransaction(payload)
    if response == 'Sucesso.':
         return {'status':'Sucesso.'}
    
    elif response == 'Erro no banco de dados.':
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"Erro interno ao acessar o banco de dados."
                          
        )
   
        
@transaction_router.patch("/update-status")
def alterTransactionStatus(payload : TransactionStatus):
    
    try:
        success = AlterTransaction.alterTransaction(payload)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transação com o ID {payload.transaction_id} não foi encontrada no sistema."
            )
            
        return {"status": "Sucesso.", 
                "message": "Status atualizado com sucesso."}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"Erro interno ao acessar o banco de dados: {str(e)}"
                            )