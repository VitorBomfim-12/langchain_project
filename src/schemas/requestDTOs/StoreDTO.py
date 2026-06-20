import pydantic,re,decimal
from pydantic import BaseModel,field_validator,Field
from decimal import Decimal


class StoreDTO(BaseModel):
    storeName:str = Field(strip_whitespace=True)
    cnpj:str = Field(strip_whitespace=True)
    mccCode:str = Field(strip_whitespace=True)
    transactionValueLimit: Decimal = Field(max_digits=19, decimal_places=4)
    location:str 
