from fastapi import APIRouter
from datetime import datetime
from first_project.services.selectQuerys import ActiveStoreQuery
from first_project.services.selectQuerys import LimitValue
from first_project.services.insertQuerys import InsertTransaction
from first_project.models.TransactionStatusEnum import StatusEnum
from first_project.services.selectQuerys.SelectStoreLocation import StoreLocation
from first_project.models.RiskEnum import RiskEnum
from first_project.services.calcHaversine import calcHaversine
from decimal import Decimal
from fastapi import APIRouter, HTTPException
from first_project.schemas.requestDTOs.TransactionDTO import TransactionDTO
from langchain.chat_models import init_chat_model

transaction_router = APIRouter(prefix="/transaction",tags=['Transaction routes'])

@transaction_router.post("/insert")
async def insertTransaction(payload: TransactionDTO):

    if not ActiveStoreQuery.ActiveStore(payload.storeID):
        message = 'Estabelecimento inativo.'
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

    storeInfo = StoreLocation.GetLocation(payload.storeID)

    dStoreTransaction = calcHaversine(payload.location[0],
                                      payload.location[1],
                                      storeInfo['lat'],
                                      storeInfo['lon'])

    if dStoreTransaction > storeInfo['fence_dis']:
        message = f'Transação suspeita: cerca eletrônica violada, distância de {dStoreTransaction:.2f} metros.'
        status = StatusEnum.PENDING
        risk = RiskEnum.HIGH
    
        
    payload.status = status
    payload.reason = message
    payload.risk = risk
    
    llm = init_chat_model('google_genai:gemini-2.0-flash')
    messages: list[BaseMessage] =[]
    systemMessage = SystemMessage(

        '''
            Você é um agente de IA responsável por analisar transações financeiras e estabelecimentos,
        a fim de gerar relátorios que indiquem possíveis fraudes e mostre estabelecimentos suspeitos.
        nessas análises, você deve levar em consideração a localização dos estabelecimentos, valores
        médios das transações, CPF dos compradores, CPF dos donos dos estabelecimentos, intervalo de 
        tempo entre transações e indíce de chargeback dos estabelecimentos.
            Seu objetivo é classificar se as transações são suspeitas com base em informações detalhadas
        que lhe serão fornecidas por funções python que vão lhe fornecer relátorios, com as mais diversas
        informações sobre os estabelecimentos e as transações.
            Você tem acessos a ferramentas, com base nos status fornecidos na humanMessage, use as tools 
        identificar possíveis fraudes
        '''
        
    )
    APImessage = HumanMessage(

        f'''-Detalhes da transação-\n
        valor:{payload.value}
        data:{payload.data}'''
    )
    dbResponse = insertTransaction(payload)
    if dbResponse == "Erro no banco de dados":
        return{'mensagem':'Erro no banco de dados.'}
        
    
    
    
