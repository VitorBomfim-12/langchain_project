import pydantic,re
from pydantic import BaseModel,Field, field_validator
from decimal import Decimal
from datetime import datetime


class Transaction(BaseModel):
    value: Decimal = Field(max_digits=19, decimal_places=4, gt=0)
    data : datetime
    cpf : str       
    location : str
    storeID: int

    @field_validator("cpf")
    @classmethod
    def validate_cpf_format(cls, v: str) -> str:
        # Limpa o CPF e verifica se tem 11 dígitos
        cpfClean = re.sub(r'\D', '', v)
        if len(cpfClean) != 11:
            raise ValueError('CPF deve conter 11 dígitos numéricos')
        return cpfClean