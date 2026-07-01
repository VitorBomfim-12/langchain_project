from pydantic import BaseModel,Field
from src.models.RiskEnum import RiskEnum

class agentResponse(BaseModel):
    storeRiskChargeback :str = Field(description="Definir o risco para antecipação de crédito proveniente de vendas")
    storeCredit:str = Field(description="Definir se o estabelecimento está apto a captar crédito.")
    generalRisk: RiskEnum = Field(description="Classifique conforme o Enum, o risco geral do estabelecimento.")
    reason:str = Field(description="""Explique de maneira curta e objetiva as razões pelas quais os status foram definidos,
    cite estatísticas e padrões encontrados.""")