from fastapi import APIRouter,HTTPException,status
from src.schemas.requestDTOs.OwnerDTO import OwnerDTO
from src.schemas.requestDTOs.StoreDTO import StoreDTO
from src.services.insertQuerys.InsertOwner import insertOwner
from src.services.insertQuerys.InsertStore import insertStore
from src.services.selectQuerys.ChargebackPercent import selectChargebackPercent
from src.services.selectQuerys.SelectAVGValue import getAVGValue
from src.models.RiskEnum import RiskEnum
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.graph import START,END,StateGraph
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama
from typing import TypedDict
from pydantic import BaseModel

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
    storeID:int
    reason:str 
    response: str
    storeReputation : str
    storeRisk : RiskEnum
    storePoints: int

tools =[getAVGValue,selectChargebackPercent]
model = ChatOllama(model="llama3").bind_tools(tools)

def modelCall(state: AgentState) -> AgentState:

    system_prompt = SystemMessage(content = '''Você é um agente de IA responsável por analisar lojas,ce
    definir determinados parâmetros para que uma empresa forncedora de máquinas de pagamento (POS)
    Você deve analizar:
    -Índices de chargeback, valor médio das transações, desvio padrão do valor médio das transações,
    CPF que mais comprou na loja,volume de transações por data, compras feitas por CPFs de donos.
    -Para efetuar estas análises, utilize as Tools disponíveis.
                                  
    O que você deve definir:
    -Se o estabelecimento é seguro ou não para que a antecipação de crédito (chargeback) 
    das compras seja feito.
    -estabelecimento está ápito e atende critérios para obtenção de crédito
    
        Guia de raciocinio:
            Utilize as Tools com o ID da loja para chamar as Tools e obter informações das lojas.
            Utilize o resultado das Tools para tomar decisões.
            Caso não haja dados disponíveis, informe em sua resposta que há falta de dados.''')
    
    response = model.invoke([system_prompt] + state['reason'])
   
    return {'messages':[response.content]}

def toolsLoop(state:AgentState) -> AgentState:
    lastMessage = state["response"]
    if not lastMessage[-1].tool_calls:
        return 'end'
    return 'continue'


toolNode = ToolNode(tools=tools)

graph = StateGraph(AgentState)
graph.add_node('model call', modelCall)
graph.add_node('tools loop',toolsLoop)
graph.add_node('tools node', toolNode)

graph.add_edge(START,'model call')
graph.add_conditional_edges(
    'model call',
    toolsLoop,
    {'continue':'tools node',
     'end':END}

)
graph.add_edge('tools node', 'model call')
app = graph.compile()

@store_and_owner_router.put("/analyze-store")
def analyzeStore(payload : StoreAnalyzeInfo):
    
    response = app.invoke({'storeID':payload.storeID,
                'reason':payload.reason})
    print(response.content)
    return {'Resposta':response.content}

    

   