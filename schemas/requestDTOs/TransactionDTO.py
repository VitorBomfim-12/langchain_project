import pydantic,re
from pydantic import BaseModel,Field, field_validator
from decimal import Decimal
from datetime import datetime, timezone
from validate_docbr import CPF


class TransactionDTO(BaseModel):
    value: Decimal = Field(max_digits=19, decimal_places=4)
    data : datetime
    cpf : str = Field(strip_whitespace=True)
    location : str 
    storeID: int

    @field_validator("cpf")
    @classmethod
    def validate_cpf_format(cls, v: str) -> str:
        validator = CPF()
        if not validator.validate(v):
            raise ValueError("CPF inválido")
        return v
    
    @field_validator('data')
    @classmethod
    def validate_date(cls,v:datetime)-> datetime:
        if v.tzinfo==None:
            v = v.replace(tzinfo=timezone.utc)

        if v > datetime.now(timezone.utc):
            raise ValueError("a transação não pode ter data futura.")
        
        return v
    
    @field_validator("location")
    @classmethod
    def validate_spatial_data(cls, v: str) -> str:
        if not v.startswith("POINT"):
            raise ValueError("A localização deve estar no formato WKT: POINT(long lat.)")
        return v
    
    @field_validator("value")
    @classmethod
    def validate_value(cls,v:Decimal)-> Decimal:
        values =[0,-1]
        zero = Decimal("0.00")
        if v.compare(zero) in values:
            raise ValueError("A transação não pode ter valor negativo ou igual a zero.")