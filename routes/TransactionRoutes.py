from fastapi import APIRouter
from datetime import datetime
from src.first_project.services.selectQuerys import ActiveStoreQuery
from first_project.services.selectQuerys import SelectLimitValue
from src.first_project.services.selectQuerys import ChargebackPercent
from src.first_project.services.insertQuerys import InsertTransaction as IT
from src.first_project.models.TransactionStatusEnum import StatusEnum
from src.first_project.services.selectQuerys.SelectStoreLocation import StoreLocation
from src.first_project.models.RiskEnum import RiskEnum
from src.first_project.services.calcHaversine import calcHaversine
from src.first_project.schemas.agentsResponseSchemas.transactionSchema import AgentResponse
from pydantic import ValidationError
from decimal import Decimal
from fastapi import APIRouter, HTTPException
from src.first_project.schemas.requestDTOs.TransactionDTO import TransactionDTO
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import BaseTool

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

transaction_router = APIRouter(prefix="/transaction",tags=['Transaction routes'])

llm = init_chat_model('google_genai:gemini-1.5-flash')

tools = [ChargebackPercent] 

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
def insertTransaction(payload: TransactionDTO):

    payload.reason = 'Null'
    payload.status = StatusEnum.APPROVED
    payload.risk = RiskEnum.LOW

    if not ActiveStoreQuery.ActiveStore(payload.storeID):
        message = 'Estabelecimento inativo.'
        status = StatusEnum.REJECTED
        risk = RiskEnum.HIGH

    elif (payload.value>SelectLimitValue.StoreLimitQuery.storeLimit(payload.storeID)):
        message = ' Limite do estabelecimento excedido.'
        status = StatusEnum.REJECTED
        risk = RiskEnum.HIGH

    elif (datetime.now().hour > 23 or datetime.now().hour < 6) and payload.value> Decimal('200.00'):
        message = 'Limite noturno excedido.'
        status = StatusEnum.PENDING
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

    

    payload.reason = message  
    payload.status = status
    payload.risk = risk
    
    if payload.status == 'PENDING' or payload.risk == 'HIGH':
     
    
        
        transactionContext =  f'''-Detalhes da transação-\n
            valor:{payload.value}\n
            data:{payload.data}\n
            cpf:{payload.cpf}\n
            location:{storeInfo["lat"],storeInfo["lon"]} latitude e longitude\n
            storeID:{payload.storeID}
            
            '''
        try: 
            response = caronte_chain.invoke({'input':transactionContext})

            payload.reason =  response.reason
            payload.status = response.status
            payload.risk = response.risk
        except Exception as e:
            pass


    dbResponse = IT(payload)
    if dbResponse == "Erro no banco de dados":
        return{'mensagem':'Erro no banco de dados.'}
        
    
    
    
