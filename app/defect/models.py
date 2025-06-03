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
    expected_completion_day = Column(Integer)  # 修繕天數
    responsible_vendor_id = Column(Integer, ForeignKey("vendors.vendor_id", ondelete="SET NULL"))  # 責任廠商ID
    previous_defect_id = Column(Integer, ForeignKey("defects.defect_id", ondelete="SET NULL"))  # 前置缺失單ID
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # 等待中、改善中、待確認、已完成、退件
    
    # Relationships
    project = relationship("Project", back_populates="defects")
    submitter = relationship("User", foreign_keys=[submitted_id], back_populates="submitted_defects")
    category = relationship("DefectCategory", back_populates="defects")
    assigned_vendor = relationship("Vendor", foreign_keys=[assigned_vendor_id], back_populates="assigned_defects")
    responsible_vendor = relationship("Vendor", foreign_keys=[responsible_vendor_id], back_populates="responsible_defects")
    previous_defect = relationship("Defect", remote_side=[defect_id], backref="next_defects", foreign_keys=[previous_defect_id])
    defect_marks = relationship("DefectMark", back_populates="defect")
    improvements = relationship("Improvement", back_populates="defect")
