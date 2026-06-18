import pydantic,re
from pydantic import BaseModel,field_validator,Field


class StoreDTO(BaseModel):
    storeName:str = Field(strip_whitespace=True)
    cnpj:str = Field(strip_whitespace=True)
    mccCode:str = Field(strip_whitespace=True)
    location:str 
