from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Permission(Base):
    __tablename__ = "permissions"
    
    permission_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"))
    user_email = Column(String, ForeignKey("users.email", ondelete="CASCADE"))
    user_role = Column(String, nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="permissions")
    user = relationship("User", foreign_keys=[user_email], back_populates="permissions")
