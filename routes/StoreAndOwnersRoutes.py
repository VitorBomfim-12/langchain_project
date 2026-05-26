from fastapi import APIRouter
from schemas.requestDTOs.OwnerDTO import OwnerDTO

store_and_owner_router = APIRouter(prefix="store-owner",tags=["store and owners"])

@store_and_owner_router.post("/insert-owner")
def insertOwnerRoute(payload : OwnerDTO):
    pass