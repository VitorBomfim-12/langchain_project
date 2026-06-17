from pydantic import BaseModel, field_validator
from langchain_project.src.models.TransactionStatusEnum import StatusEnum


class TransactionStatus(BaseModel):
    transactionID: int
    status: StatusEnum
    reason:str