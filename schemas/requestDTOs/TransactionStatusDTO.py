from pydantic import BaseModel, field_validator
from first_project.models.TransactionStatusEnum import StatusEnum


class TransactionStatus(BaseModel):
    transactionID: int
    status: StatusEnum
    reason:str