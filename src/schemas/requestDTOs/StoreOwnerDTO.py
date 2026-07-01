import pydantic,re,decimal
from pydantic import BaseModel, Field

class StoreOwner(BaseModel):
    ownerID: int = Field(description="ID único do propietário.")
    storeID: int = Field(description="ID único do estabelecimento.")