import pydantic,re
from pydantic import BaseModel,field_validator,Field
from validate_docbr import CNPJ


class StoreDTO(BaseModel):
    storeName:str = Field(strip_whitespace=True)
    cnpj:str = Field(strip_whitespace=True)
    mccCode:str = Field(strip_whitespace=True)
    location:str 

    @field_validator
    @classmethod
    def validate_cnpj(cls,v:str)->str:
        validator = CNPJ()

        if not validator.validate(v):
            raise ValueError("CNJP inválido")
        
        return v
    
    @field_validator
    @classmethod
    def clean_cnpj(cls,v:str)->str:
        return re.sub(r'\D', '', v)
