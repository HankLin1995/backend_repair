from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.improvement.models import Improvement
from app.improvement.schemas import ImprovementCreate, ImprovementUpdate
from app.user.models import User
from app.defect.models import Defect

def get_improvement(db: Session, improvement_id: int) -> Optional[Improvement]:
    """Get a single improvement by ID"""
    return db.query(Improvement).filter(Improvement.improvement_id == improvement_id).first()

def get_improvements(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    defect_id: Optional[int] = None,
    submitter_id: Optional[int] = None
) -> List[Improvement]:
    """Get a list of improvements with pagination and optional filtering"""
    query = db.query(Improvement)
    
    # Apply filters if provided
    if defect_id:
        query = query.filter(Improvement.defect_id == defect_id)
    if submitter_id:
        query = query.filter(Improvement.submitter_id == submitter_id)
    
    # Apply pagination
    query = query.order_by(Improvement.created_at.desc())
    return query.offset(skip).limit(limit).all()

def get_improvements_by_defect(db: Session, defect_id: int) -> List[Improvement]:
    """Get all improvements for a specific defect"""
    return db.query(Improvement).filter(Improvement.defect_id == defect_id).order_by(Improvement.created_at.desc()).all()

def get_improvements_by_submitter(db: Session, submitter_id: int) -> List[Improvement]:
    """Get all improvements submitted by a specific user"""
    return db.query(Improvement).filter(Improvement.submitter_id == submitter_id).order_by(Improvement.created_at.desc()).all()

def create_improvement(db: Session, improvement: ImprovementCreate) -> Improvement:
    """Create a new improvement"""
    db_improvement = Improvement(
        defect_id=improvement.defect_id,
        submitter_id=improvement.submitter_id,
        content=improvement.content,
        improvement_date=improvement.improvement_date,
        created_at=datetime.utcnow()
    )
    db.add(db_improvement)
    
    # 更新缺失狀態為「待確認」
    defect = db.query(Defect).filter(Defect.defect_id == improvement.defect_id).first()
    if defect:
        defect.status = "待確認"
    
    db.commit()
    db.refresh(db_improvement)
    return db_improvement

def update_improvement(db: Session, improvement_id: int, improvement: ImprovementUpdate) -> Optional[Improvement]:
    """Update an existing improvement"""
    db_improvement = get_improvement(db, improvement_id)
    if not db_improvement:
        return None
    
    update_data = improvement.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_improvement, key, value)
    
    db.commit()
    db.refresh(db_improvement)
    return db_improvement

def delete_improvement(db: Session, improvement_id: int) -> bool:
    """Delete an improvement"""
    db_improvement = get_improvement(db, improvement_id)
    if not db_improvement:
        return False
    
    db.delete(db_improvement)
    db.commit()
    return True

def get_improvement_with_details(db: Session, improvement_id: int) -> Optional[Dict[str, Any]]:
    """Get an improvement with related details"""
    # Query the improvement with related entities
    improvement = (
        db.query(
            Improvement,
            User.name.label("submitter_name"),
            Defect.defect_description
        )
        .join(User, Improvement.submitter_id == User.user_id, isouter=True)
        .join(Defect, Improvement.defect_id == Defect.defect_id)
        .filter(Improvement.improvement_id == improvement_id)
        .first()
    )
    
    if not improvement:
        return None
    
    improvement_obj, submitter_name, defect_description = improvement
    
    # Create result dictionary
    result = {
        "improvement_id": improvement_obj.improvement_id,
        "defect_id": improvement_obj.defect_id,
        "defect_description": defect_description,
        "submitter_id": improvement_obj.submitter_id,
        "submitter_name": submitter_name,
        "content": improvement_obj.content,
        "improvement_date": improvement_obj.improvement_date,
        "created_at": improvement_obj.created_at
    }
    
    return result
