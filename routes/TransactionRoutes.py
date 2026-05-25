from fastapi import APIRouter
from datetime import datetime
from services.selectQuerys.ActiveStoreQuery import ActiveStore
from services.selectQuerys.SelectLimitValue import StoreLimitQuery
from services.selectQuerys.ChargebackPercent import selectChargebackPercent
from services.insertQuerys.InsertTransaction import InsertTransaction as it
from models.TransactionStatusEnum import StatusEnum
from services.selectQuerys.SelectStoreLocation import StoreLocation
from models.RiskEnum import RiskEnum
from services.calcHaversine import calcHaversine
from schemas.agentsResponseSchemas.transactionSchema import AgentResponse
from pydantic import ValidationError
from decimal import Decimal
from fastapi import APIRouter, HTTPException
from schemas.requestDTOs.TransactionDTO import TransactionDTO
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import BaseTool

from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
import os

llm = init_chat_modelllm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"), # Puxa do seu .env
    temperature=0
)

tools = [selectChargebackPercent] 

prompt = ChatPromptTemplate.from_messages([
    ("system", ''' ### Instrução ###
                Você é um agente de IA responsável por analisar transações financeiras e estabelecimentos,
            a fim de gerar relátorios que indiquem possíveis fraudes e mostre estabelecimentos suspeitos.
            nessas análises, você deve levar em consideração a localização dos estabelecimentos, valores
            médios das transações, CPF dos compradores, CPF dos donos dos estabelecimentos, intervalo de 
            tempo entre transações e indíce de chargeback dos estabelecimentos.
    
                Seu objetivo é classificar se as transações são suspeitas com base em informações detalhadas
            que lhe serão fornecidas por funções python que vão lhe fornecer relátorios, com as mais diversas
            informações sobre os estabelecimentos e as transações.
                Você tem acessos a ferramentas, com base nos status fornecidos na humanMessage, use as tools para
            identificar possíveis fraudes.'''),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"), 
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

llm_formatador = llm.with_structured_output(AgentResponse, method="json_mode")

caronte_chain = agent_executor | (lambda x: f"Com base nesta investigação: {x['output']}. Formate o veredito final.") | llm_formatador
transaction_router = APIRouter(prefix="/transaction",tags=['Transaction routes'])
@transaction_router.post("/insert")

def insertTransaction(payload: TransactionDTO):
    print("TESTEEEEE")
    print(payload)

    if not ActiveStore(payload.storeID):
        message = 'Estabelecimento inativo.'
        status = StatusEnum.REJECTED
        risk = RiskEnum.HIGH

    elif payload.value>StoreLimitQuery.storeLimit(payload.storeID):
        message = 'Limite do estabelecimento excedido.'
        status = StatusEnum.PENDING
        risk = RiskEnum.HIGH

    elif (datetime.now().hour > 23 or datetime.now().hour < 6) and payload.value> Decimal('200.00'):
        message = 'Limite noturno excedido.'
        status = StatusEnum.PENDING
        risk = RiskEnum.HIGH

    elif payload.value <= Decimal('2.00'):
        message = 'Transação suspeita: valor jabaixo do piso mínimo de segurança.'
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

    payload.reason = message  
    payload.status = status
    payload.risk = risk
    
    if payload.status == 'PENDING' or payload.risk == 'HIGH':
         
        transactionContext =  f'''-Detalhes da transação-\n
            valor:{payload.value}\n
            data:{payload.data}\n
            cpf:{payload.cpf}\n
            location:{storeInfo["lat"],storeInfo["lon"]} latitude e longitude\n
            storeID:{payload.storeID}\n
            razão dos status:{payload.reason}
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


    response =it.insertTransaction(payload)
    if response != 'Sucesso.':
        return {'status':'erro'}
    return {'status':'Sucesso.'}
        
    
    
    
