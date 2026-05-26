from pydantic import BaseModel,Field
from models.RiskEnum import RiskEnum
from models.TransactionStatusEnum import StatusEnum

class AgentResponse(BaseModel):
    status: StatusEnum
    risk: RiskEnum
    reason:str = Field(description="Insira a razão as decisões tomadas, escreva em português")