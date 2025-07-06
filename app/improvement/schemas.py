from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

# Base Improvement Schema
class ImprovementBase(BaseModel):
    defect_id: int
    content: str

# Schema for creating a new Improvement
class ImprovementCreate(ImprovementBase):
    submitter_id: Optional[int] = None
    improvement_date: date

# Schema for creating an improvement via unique code (without defect_id)
class ImprovementCreateByUniqueCode(BaseModel):
    content: str
    submitter_id: Optional[int] = None
    improvement_date: date

# Schema for updating an existing Improvement
class ImprovementUpdate(BaseModel):
    content: Optional[str] = None
    improvement_date: Optional[date] = None

# Schema for Improvement in response
class ImprovementOut(ImprovementBase):
    improvement_id: int
    submitter_id: Optional[int] = None
    improvement_date: date
    created_at: datetime

    model_config = {"from_attributes": True}
