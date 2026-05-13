import pydantic
from pydantic import BaseModel, field_validator, Field
from validate_docbr import CPF
class Owner(BaseModel):
    name:str 
    cpf:str

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls,v:str)->str:
        validator = CPF()

        if not validator.validate(v):
            raise ValueError("CPF inválido.")
        
        return v


    @field_validator(name)
    @classmethod
    def validate_cnpj(cls,v:str)->str:
        
        if not v:
            raise ValueError("Nome invalido.")
        
        return v