from pydantic import BaseModel, field_validator, Field
from langchain_project.src.models.RiskEnum import RiskEnum

class StoreMetric(BaseModel):
    storeID: int
    riskLevel: RiskEnum
    totalChargebacks: int
    
    
   