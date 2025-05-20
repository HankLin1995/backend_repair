from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Defect(Base):
    __tablename__ = "defects"
    
    defect_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"))
    submitted_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    defect_category_id = Column(Integer, ForeignKey("defect_categories.defect_category_id", ondelete="SET NULL"))
    defect_description = Column(Text)
    assigned_vendor_id = Column(Integer, ForeignKey("vendors.vendor_id", ondelete="SET NULL"))
    repair_description = Column(Text)
    repair_completed_at = Column(DateTime)
    confirmation_status = Column(String)
    confirmation_time = Column(DateTime)
    confirmer_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="defects")
    submitter = relationship("User", foreign_keys=[submitted_id], back_populates="submitted_defects")
    confirmer = relationship("User", foreign_keys=[confirmer_id], back_populates="confirmed_defects")
    category = relationship("DefectCategory", back_populates="defects")
    vendor = relationship("Vendor", back_populates="defects")
    defect_marks = relationship("DefectMark", back_populates="defect")
    photos = relationship("Photo", back_populates="defect")
