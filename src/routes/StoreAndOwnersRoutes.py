from fastapi import APIRouter,HTTPException,status
from src.schemas.requestDTOs.OwnerDTO import OwnerDTO
from src.schemas.requestDTOs.StoreDTO import StoreDTO
from src.schemas.requestDTOs.StoreAnalysisDTO import StoreAnalyzeInfo
from src.services.insertQuerys.InsertOwner import insertOwner
from src.services.insertQuerys.InsertStore import insertStore
from src.agents.agent import create_caronte_agent
from src.agents.prompts import store_analysis_prompt
from src.schemas.responseDTOs.AgentResponse import agentResponse

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


@store_and_owner_router.post("/analyze-store")
def analyzeStore(payload : StoreAnalyzeInfo):
    print(payload)
   

    inputs = {f"""
          'storeID': {payload.storeID}, 
          'reason': {payload.reason},
          'period': {payload.period}
            """}
    try:
        agent = create_caronte_agent(store_analysis_prompt,agentResponse)
        result = agent.invoke({"messages":[{"role":"user",
                                            "content":inputs}]})
        print (result)
        return {"status":"Sucesso.",
                "resultado da analise":result["structured_response"]}
    
    except Exception as e:
        print (e)
        return {"status":f"erro{e}"}

   