from pydantic import BaseModel, field_validator, Field
from validate_docbr import CPF
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
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
    def validate_cnpj(cls,v:date)->date:
        if v > datetime.now(): raise ValueError("Idade inválida.")
        if v - relativedelta(year=18) < relativedelta(18):raise ValueError('''Pessoas com idade menor 
        que 18 não podem ser cadastras como propietárias.''')
        
        return v