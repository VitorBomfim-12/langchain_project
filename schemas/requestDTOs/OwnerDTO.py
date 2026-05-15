from pydantic import BaseModel, field_validator, Field
from validate_docbr import CPF
from datetime import date
class OwnerDTO(BaseModel):
    name:str = Field(strip_whitespace=True)
    cpf:str = Field(strip_whitespace=True)
    birthday : date

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls,v:str)->str:
        validator = CPF()

        if not validator.validate(v):
            raise ValueError("CPF inválido.")
        
        return v


    @field_validator("name")
    @classmethod
    def validate_cnpj(cls,v:str)->str:
        
        if not v or not v.strip():
            raise ValueError("Nome invalido.")
        
        return v