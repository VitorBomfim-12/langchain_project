from pydantic import BaseModel, field_validator, Field
from src.first_project.models.RiskEnum import RiskEnum

class StoreMetric(BaseModel):
    storeID: int
    riskLevel: RiskEnum
    totalChargebacks: int
    
    
   