from pydantic import BaseModel, Field, field_validator
from validate_docbr import CPF

class Blacklist(BaseModel):
    identifierCPF:str = Field(strip_whitespace=True)
    severityLevel:str  = Field(strip_whitespace=True)
    storeIdFk:int
    reason:str

    @field_validator('identifierCPF')
    @classmethod
    def validate_cnpj(cls,v:str)->str:
        validator = CPF()

        if not validator.validate(v):
            raise ValueError("CPF inválido")
        
        return v