from pydantic import BaseModel, field_validator, Field
from src.models.RiskEnum import RiskEnum

class StoreMetric(BaseModel):
    storeID: int
    riskLevel: RiskEnum
    totalChargebacks: int
    
    
   