from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Improvement(Base):
    __tablename__ = "improvements"
    
    improvement_id = Column(Integer, primary_key=True, index=True)
    defect_id = Column(Integer, ForeignKey("defects.defect_id", ondelete="CASCADE"))
    submitter_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    content = Column(Text)
    improvement_date = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    defect = relationship("Defect", back_populates="improvements")
    submitter = relationship("User", back_populates="submitted_improvements")
    confirmations = relationship("Confirmation", back_populates="improvement")
