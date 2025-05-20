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
    
    # Relationships
    defects = relationship("Defect", back_populates="vendor")
