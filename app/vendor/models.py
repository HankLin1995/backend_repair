from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Vendor(Base):
    __tablename__ = "vendors"
    
    vendor_id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String, nullable=False)
    contact_person = Column(String)
    phone = Column(String)
    responsibilities = Column(Text)
    email = Column(String)
    line_id = Column(String)
    
    # Relationships
    assigned_defects = relationship("Defect", foreign_keys="Defect.assigned_vendor_id", back_populates="assigned_vendor")
    responsible_defects = relationship("Defect", foreign_keys="Defect.responsible_vendor_id", back_populates="responsible_vendor")
