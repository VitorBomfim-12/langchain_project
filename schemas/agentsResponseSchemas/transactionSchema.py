from pydantic import BaseModel
from models.RiskEnum import RiskEnum
from models.TransactionStatusEnum import StatusEnum

class AgentResponse(BaseModel):
    status: StatusEnum
    risk: RiskEnum
    reason:str