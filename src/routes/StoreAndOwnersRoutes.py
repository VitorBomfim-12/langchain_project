from fastapi import APIRouter,HTTPException,status
from src.schemas.requestDTOs.OwnerDTO import OwnerDTO
from src.schemas.requestDTOs.StoreDTO import StoreDTO
from src.schemas.requestDTOs.StoreAnalysisDTO import StoreAnalyzeInfo
from src.services.insertQuerys.InsertOwner import insertOwner
from src.services.insertQuerys.InsertStore import insertStore
from src.services.selectQuerys.ChargebackPercent import selectChargebackPercent
from src.services.selectQuerys.SelectAVGValue import getAVGValue
from src.models.RiskEnum import RiskEnum
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage,BaseMessage,AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START,END,StateGraph
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel,Field
from typing import TypedDict,Annotated,Sequence,Optional
from datetime import date
import os, dotenv,json
dotenv.load_dotenv()
store_and_owner_router = APIRouter(prefix="/clients",tags=["store and owners"])

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


class AgentState(TypedDict):
    storeID:int
    reason:str
    period:list[date]
    messages: Annotated[Sequence[BaseMessage], add_messages]
    agentAnalysis:Optional[dict] = None

tools =[getAVGValue,selectChargebackPercent]


class agentResponse(BaseModel):
    storeRiskChargeback :str = Field(description="Definir o risco para antecipação de crédito proveniente de vendas")
    storeCredit:str = Field(description="Definir se o estabelecimento está apto a captar crédito.")
    generalRisk: RiskEnum = Field(description="Classifique conforme o Enum, o risco geral do estabelecimento.")
    reason:str = Field(description="""Explique de maneira curta e objetiva as razões pelas quais os status foram definidos,
    cite estatísticas e padrões encontrados.""")

system_prompt = '''Você é um agente de IA responsável por analisar lojas e
    definir determinados parâmetros para uma empresa fornecedora de máquinas de pagamento (POS).
    
    Para efetuar as análises de índices de chargeback e valor médio, utilize as Tools disponíveis passando o ID da loja e o período de análise.
                                  
    O que você deve definir:
    - Se o estabelecimento é seguro para antecipação de crédito.
    - Se o estabelecimento está apto para obtenção de crédito.
    
    Guia de raciocínio:
    - Use o ID da loja e as ferramentas para obter informações.
    - Use, OBRIGATORIAMENTE, as tools que lhe foram passadas'''
    
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"))

agent = create_agent(model=model,
                    system_prompt=system_prompt,
                    tools=tools,
                    response_format= agentResponse)


@store_and_owner_router.post("/analyze-store")
def analyzeStore(payload : StoreAnalyzeInfo):
    print(payload)

    inputs = {f"""
          'storeID': {payload.storeID}, 
          'reason': {payload.reason},
          'period': {payload.period}
            """}
    try:
        result = agent.invoke({"messages":[{"role":"user",
                                            "content":inputs}]})
        print (result["structured_response"])
        return {"status":"Sucesso.",
                "resultado da analise":result["structured_response"]}
    
    except Exception as e:
        print (e)
        return {"status":f"erro{e}"}

   