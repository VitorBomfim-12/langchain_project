from pydantic import BaseModel, field_validator, Field
from datetime import date,datetime
from services.ageVerify import isOver18 
class OwnerDTO(BaseModel):
    name:str = Field(description="Nome do propietário",strip_whitespace=True)
    cpf:str = Field(description="CPF do propietário",strip_whitespace=True)
    birthday : date = Field(description="Data de nascimento.")


    @field_validator("name")
    @classmethod
    def validate_cnpj(cls,v:str)->str:
        
        if not v or not v.strip():
            raise ValueError("Nome invalido.")
        
        return v
    
    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls,v:date)->date:
       if not isOver18(v):
        raise ValueError("Idade inválida.")
       
       return v