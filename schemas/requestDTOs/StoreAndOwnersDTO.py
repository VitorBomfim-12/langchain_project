from pydantic import BaseModel, Field, field_validator

class StoreAndOwnersDTO(BaseModel):
    ownerID:int
    storeID:int