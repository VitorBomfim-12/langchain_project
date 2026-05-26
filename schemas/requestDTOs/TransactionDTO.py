import pydantic,re
from pydantic import BaseModel,Field, field_validator
from decimal import Decimal
from datetime import datetime, timezone
from models.TransactionStatusEnum import StatusEnum
from models.RiskEnum import RiskEnum


class TransactionDTO(BaseModel):
    value: Decimal = Field(max_digits=19, decimal_places=4)
    data : datetime
    cpf : str = Field(strip_whitespace=True)
    location :list
    status: StatusEnum
    risk: RiskEnum
    reason:str
    storeID: int

    @field_validator('data')
    @classmethod
    def validate_date(cls,v:datetime)-> datetime:
        if v.tzinfo==None:
            v = v.replace(tzinfo=timezone.utc)

        if v > datetime.now(timezone.utc):
            raise ValueError("a transação não pode ter data futura.")
        
        return v

    