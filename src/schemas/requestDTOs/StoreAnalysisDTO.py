from pydantic import BaseModel

class StoreAnalyzeInfo(BaseModel):
    storeID:int
    period:list
    reason:str 