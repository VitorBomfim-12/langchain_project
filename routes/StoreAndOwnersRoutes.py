from fastapi import APIRouter,HTTPException,status
from schemas.requestDTOs.OwnerDTO import OwnerDTO
from services.insertQuerys.InsertOwner import insertOwner

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
   