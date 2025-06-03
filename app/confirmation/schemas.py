from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Base Confirmation Schema
class ConfirmationBase(BaseModel):
    improvement_id: int
    status: str  # 接受、退回、未確認

# Schema for creating a new Confirmation
class ConfirmationCreate(ConfirmationBase):
    confirmer_id: int
    comment: Optional[str] = None
    confirmation_date: str

# Schema for updating an existing Confirmation
class ConfirmationUpdate(BaseModel):
    status: Optional[str] = None
    comment: Optional[str] = None
    confirmation_date: Optional[str] = None

# Schema for Confirmation in response
class ConfirmationOut(ConfirmationBase):
    confirmation_id: int
    confirmer_id: int
    comment: Optional[str] = None
    confirmation_date: str
    created_at: datetime

    model_config = {"from_attributes": True}
