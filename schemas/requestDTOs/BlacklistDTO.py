from pydantic import BaseModel, Field, field_validator
from models.RiskEnum import RiskEnum

class BlacklistDTO(BaseModel):
    identifierCPF:str = Field(strip_whitespace=True)
    severityLevel: RiskEnum
    storeIdFk:int
    reason:str

    
    