from pydantic import BaseModel, Field

class AnalysisResponse(BaseModel):
    sector: str = Field(..., description="The sector that was analyzed")
    report: str = Field(..., description="Markdown formatted analysis report")

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")
