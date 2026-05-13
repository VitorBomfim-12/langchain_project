from pydantic import BaseModel, Field, field_validator
from validate_docbr import CPF
from models.RiskEnum import RiskEnum

class Blacklist(BaseModel):
    identifierCPF:str = Field(strip_whitespace=True)
    severityLevel: RiskEnum
    storeIdFk:int
    reason:str

    @field_validator('identifierCPF')
    @classmethod
    def validate_cpf(cls,v:str)->str:
        validator = CPF()

        if not validator.validate(v):
            raise ValueError("CPF inválido.")

        return v
    
    