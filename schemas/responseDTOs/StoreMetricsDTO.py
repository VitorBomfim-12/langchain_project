from pydantic import BaseModel, field_validator, Field
from models.RiskEnum import RiskEnum

class StoreMetric(BaseModel):
    storeID: int
    riskLevel: RiskEnum
    totalChargebacks: int
    
    
   