from fastapi import APIRouter,HTTPException,status
from datetime import datetime
from services.selectQuerys.ActiveStoreQuery import ActiveStore
from services.selectQuerys.SelectLimitValue import StoreLimitQuery
from services.selectQuerys.ChargebackPercent import selectChargebackPercent
from services.selectQuerys.SelectValueByCPF import selectValueByCPF
from services.insertQuerys.InsertTransaction import InsertTransaction as it
from models.TransactionStatusEnum import StatusEnum
from services.selectQuerys.SelectStoreLocation import StoreLocation
from models.RiskEnum import RiskEnum
from services.calcHaversine import calcHaversine
from schemas.agentsResponseSchemas.transactionSchema import AgentResponse
from decimal import Decimal
from schemas.requestDTOs.TransactionDTO import TransactionDTO
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

import os

from services.updateQuerys.TransactionStatus import AlterTransaction
from schemas.requestDTOs.TransactionStatusDTO import TransactionStatus

llm = init_chat_modelllm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY"), 
    temperature=0
)

tools = [selectChargebackPercent,selectValueByCPF] 
transaction_router = APIRouter(prefix="/transaction",tags=['Transaction routes'])

@transaction_router.post("/insert")
def insertTransaction(payload: TransactionDTO):
    
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

    payload.reason = message  
    payload.status = statusTransaction
    payload.risk = risk
    
    if payload.status == 'PENDING' or payload.risk == 'HIGH':
         
        transactionContext =  f'''-Detalhes da transação-\n
            valor:{payload.value}\n
            data:{payload.data}\n
            cpf:{payload.cpf}\n
            location:{storeInfo["lat"],storeInfo["lon"]} latitude e longitude\n
            storeID:{payload.storeID}\n
            razão dos status:{payload.reason}\n
            Alertas gerados:{message}\n
            '''
        try: 
            response = caronte_chain.invoke({'input':transactionContext})

            payload.reason =  response.reason
            payload.status = response.status
            payload.risk = response.risk
            
        except Exception as e:

            payload.reason =f'O agente não foi capaz de analisar a transação, erro:{e}'
            payload.status = StatusEnum.PENDING
            payload.risk = RiskEnum.HIGH
            print(e)

    response =it.insertTransaction(payload)
    if response == 'Sucesso.':
         return {'status':'Sucesso.'}
    
    elif response == 'Erro no banco de dados.':
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"Erro interno ao acessar o banco de dados: {str(e)}"
                          
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