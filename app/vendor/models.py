from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Vendor(Base):
    __tablename__ = "vendors"
    
    vendor_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False)
    vendor_name = Column(String, nullable=False)
    contact_person = Column(String)
    phone = Column(String)
    responsibilities = Column(Text)
    email = Column(String)
    line_id = Column(String)
    unique_code = Column(String, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="vendors")
    assigned_defects = relationship("Defect", foreign_keys="Defect.assigned_vendor_id", back_populates="assigned_vendor")
    responsible_defects = relationship("Defect", foreign_keys="Defect.responsible_vendor_id", back_populates="responsible_vendor")
