from fastapi import APIRouter,HTTPException,status
from langchain_project.src.schemas.requestDTOs.OwnerDTO import OwnerDTO
from langchain_project.src.schemas.requestDTOs.StoreDTO import StoreDTO
from langchain_project.src.services.insertQuerys.InsertOwner import insertOwner
from langchain_project.src.services.insertQuerys.InsertStore import insertStore
from langchain_project.src.services.selectQuerys import ChargebackPercent,SelectAVGValue
from langchain_project.src.models.RiskEnum import RiskEnum
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from typing import TypedDict
from pydantic import BaseModel
import os
store_and_owner_router = APIRouter(prefix="/store-owner",tags=["store and owners"])

@store_and_owner_router.post("/insert-owner")
def insertOwnerRoute(payload : OwnerDTO):
    response = insertOwner(payload)
    
    if response == "Erro no banco de dados.":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"Erro interno ao acessar o banco de dados."         
        )
    return {"status":"sucesso."}

@store_and_owner_router.post("/insert-store")
def insertStoreRoute(payload: StoreDTO):
    response = insertStore(payload)

    if response == "Erro no banco de dados.":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"Erro interno ao acessar o banco de dados."         
        )
    return {"status":"sucesso."}

class StoreAnalyzeInfo(BaseModel):
    storeID:int
    reason:str 

class AgentState(TypedDict):
    storeReputation : str
    storeRisk : RiskEnum
    storePoints: int

tools =[SelectAVGValue,ChargebackPercent]
model = init_chat_modelllm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY"), 
    temperature=0
).bind_tools(tools)

def model_call():
    system_prompt = SystemMessage(content = '''Você é um agente de IA responsável por analisar lojas,ce
    definir determinados parâmetros para que uma empresa forncedora de máquinas de pagamento (POS)
    Você deve analizar:
    -Índices de chargeback, valor médio das transações, desvio padrão do valor médio das transações,
    CPF que mais comprou na loja,volume de transações por data, compras feitas por CPFs de donos.
    -Para efetuar estas análises, utilize as Tools disponíveis.
                                  
    -O que você deve definir:
    Se o estabelecimento é seguro ou não para que a antecipação de crédito das compras seja feito, se o
    estabelecimento está ápito e atende critérios para obtenção de crédito
    
        Guia:
            Utilize o resultado das Tools para tomar decisões.
            Não alucine, caso não haja dados disponíveis, informe em sua resposta
                                                               ''')
    

@store_and_owner_router.put("/analyze-store")
def analyzeStore(payload : StoreAnalyzeInfo):
    pass


    

   