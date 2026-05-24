from fastapi import APIRouter
from datetime import datetime
from src.first_project.services.selectQuerys import ActiveStoreQuery
from src.first_project.services.selectQuerys import LimitValue
from src.first_project.services.selectQuerys import ChargebackPercent
from src.first_project.services.insertQuerys import InsertTransaction as IT
from src.first_project.models.TransactionStatusEnum import StatusEnum
from src.first_project.services.selectQuerys.SelectStoreLocation import StoreLocation
from src.first_project.models.RiskEnum import RiskEnum
from src.first_project.services.calcHaversine import calcHaversine
from pydantic import ValidationError
from decimal import Decimal
from fastapi import APIRouter, HTTPException
from src.first_project.schemas.requestDTOs.TransactionDTO import TransactionDTO
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import BaseTool

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
    
    payload.reason = message  
    payload.status = status
    payload.risk = risk
    
    if payload.status == 'PENDING' or payload.risk == 'HIGH':
        llm = init_chat_model('google_genai:gemini-2.0-flash')
        tools: list[BaseTool] =[ChargebackPercent]
        toolsByName = {tool.name: tool for tool in tools}
        llmWithTools = llm.bind_tools(tools)
    
       
        systemMessage = SystemMessage(
    
            '''
             ### Instrução ###
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
             
                ### Exemplo de saída ###
                ## Faça um JSON puro, contendo estes itens e suas chaves ##
                ## Utilize apenas aspas duplas ##
                ## NÃO adicione blocos de código (como ```json) ou qualquer texto antes e depois do JSON. Devolva apenas o objeto: ##
                ## Utilize obrigatóriamente alguma função que lhe foi passada##
                {
                "status": "INSIRA AQUI UM DOS TRÊS: APPROVED, REJECTED OU PENDING",
                "risk": "INSIRA AQUI UM DOS TRÊS: LOW, MEDIUM OU HIGH",
                "reason": "Sua justificativa detalhada, porém direta e breve, explicando o motivo das decisões de risco e status."
                 }
            '''
            
        )
        APImessage = HumanMessage(
    
            f'''-Detalhes da transação-\n
            valor:{payload.value}\n
            data:{payload.data}\n
            cpf:{payload.cpf}\n
            location:{storeInfo["lat"],storeInfo["lon"]} latitude e longitude\n
            
            '''
        )
        
        messages : list[BaseMessage] = [systemMessage,APImessage]
        llmResponse = llmWithTools.invoke(messages)
        messages.append(llmResponse)
        if isinstance(llm, AIMessage) and getattr(llmResponse, 'tool_calls, None'):
            call = llmResponse.tool_calls[-1]
            name, args, id_ = call['name'], call['args'], call['id']
    
            try:
                content = toolsByName[name].invoke(args)
            except (KeyError,IndexError, TypeError, ValidationError,ValueError) as e:
                content = f'Corrija este erro:{e}'
            
            toolMessage= ToolMessage(content=content)

    dbResponse = IT(payload)
    if dbResponse == "Erro no banco de dados":
        return{'mensagem':'Erro no banco de dados.'}
        
    
    
    
