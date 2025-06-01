from pydantic import BaseModel
from typing import Optional, List

class VendorBase(BaseModel):
    vendor_name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    responsibilities: Optional[str] = None
    email: Optional[str] = None
    line_id: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class VendorUpdate(BaseModel):
    vendor_name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    responsibilities: Optional[str] = None
    email: Optional[str] = None
    line_id: Optional[str] = None

class VendorOut(VendorBase):
    vendor_id: int
    
    model_config = {"from_attributes": True}

class VendorWithDefectCountOut(VendorOut):
    defect_count: int
