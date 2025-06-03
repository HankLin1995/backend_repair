from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Confirmation(Base):
    __tablename__ = "confirmations"
    
    confirmation_id = Column(Integer, primary_key=True, index=True)
    improvement_id = Column(Integer, ForeignKey("improvements.improvement_id", ondelete="CASCADE"))
    confirmer_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    comment = Column(Text)
    confirmation_date = Column(String)
    status = Column(String)  # 接受、退回、未確認
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    improvement = relationship("Improvement", back_populates="confirmations")
    confirmer = relationship("User", back_populates="confirmations")
