from fastapi import APIRouter,HTTPException,status
from src.schemas.requestDTOs.OwnerDTO import OwnerDTO
from src.schemas.requestDTOs.StoreDTO import StoreDTO
from src.services.insertQuerys.InsertOwner import insertOwner
from src.services.insertQuerys.InsertStore import insertStore
from src.services.selectQuerys.ChargebackPercent import selectChargebackPercent
from src.services.selectQuerys.SelectAVGValue import getAVGValue
from src.models.RiskEnum import RiskEnum
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage,BaseMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START,END,StateGraph
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama
from typing import TypedDict,Annotated,Sequence
from pydantic import BaseModel
from datetime import date
import os, dotenv
dotenv.load_dotenv()
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
    period:list
    reason:str 

class AgentState(TypedDict):
    storeID:int
    reason:str
    period:list
    messages: Annotated[Sequence[BaseMessage], add_messages]

tools =[getAVGValue,selectChargebackPercent]

model = init_chat_modelllm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY"), 
    temperature=0
).bind_tools(tools)

def modelCall(state: AgentState) -> AgentState: 

    system_prompt = '''Você é um agente de IA responsável por analisar lojas e
    definir determinados parâmetros para uma empresa fornecedora de máquinas de pagamento (POS).
    
    Para efetuar as análises de índices de chargeback e valor médio, utilize as Tools disponíveis passando o ID da loja e o período de análise.
                                  
    O que você deve definir:
    - Se o estabelecimento é seguro para antecipação de crédito.
    - Se o estabelecimento está apto para obtenção de crédito.
    
    Guia de raciocínio:
    - Use o ID da loja e as ferramentas para obter informações.
    - Use, OBRIGATORIAMENTE, as tools que lhe foram passadas'''
    current_messages = state.get('messages', [])
        
    if not current_messages:
            
            user_content = f'''ID da Loja a ser analisada: {state['storeID']}\n
            Motivo da análise: {state['reason']}\n
            data inicial: {state["period"][0]}\n
            data final: {state["period"][1]}\n'''
            messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_content)]
    else:
        messages = [SystemMessage(content=system_prompt)] + list(current_messages)

    state['messages'] = messages 
    
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}
   
   
def toolsLoop(state:AgentState) -> AgentState:
    lastMessage = state["messages"]
    if not lastMessage[-1].tool_calls:
        return 'end'
    else:
        return 'continue'


toolNode = ToolNode(tools=tools)

graph = StateGraph(AgentState)
graph.add_node('model call', modelCall)
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

@store_and_owner_router.get("/analyze-store")
def analyzeStore(payload : StoreAnalyzeInfo):
    print(payload)
    inputs = {
          'storeID': payload.storeID, 
          'reason': payload.reason,
          'period': payload.period
      }
    
    final_state = app.invoke(inputs) 
    final_message = final_state["messages"][-1]
      
    print(final_message.content)
    return {'Resposta': final_message.content}
  
    

   