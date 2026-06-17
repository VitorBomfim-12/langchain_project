from pydantic import BaseModel,Field
from langchain_project.src.models.RiskEnum import RiskEnum
from langchain_project.src.models.TransactionStatusEnum import StatusEnum

class AgentResponse(BaseModel):
    status: StatusEnum
    risk: RiskEnum
    reason:str = Field(description="Insira a razão as decisões tomadas, escreva em português")