from pydantic import BaseModel


class ApprovalAnalysis(BaseModel):
    summary: str
    strengths: list[str]
    concerns: list[str]


class RiskAnalysis(BaseModel):
    risk_level: str
    risk_factors: list[str]


class CreditHistoryAnalysis(BaseModel):
    summary: str
    observations: list[str]


class InvestigationReport(BaseModel):
    executive_summary: str
    recommendation: str
    strengths: list[str]
    risks: list[str]