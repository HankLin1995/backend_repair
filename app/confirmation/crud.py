from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.confirmation.models import Confirmation
from app.confirmation.schemas import ConfirmationCreate, ConfirmationUpdate
from app.user.models import User
from app.improvement.models import Improvement
from app.defect.models import Defect

def get_confirmation(db: Session, confirmation_id: int) -> Optional[Confirmation]:
    """Get a single confirmation by ID"""
    return db.query(Confirmation).filter(Confirmation.confirmation_id == confirmation_id).first()

def get_confirmations(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    improvement_id: Optional[int] = None,
    confirmer_id: Optional[int] = None,
    status: Optional[str] = None
) -> List[Confirmation]:
    """Get a list of confirmations with pagination and optional filtering"""
    query = db.query(Confirmation)
    
    # Apply filters
    if improvement_id:
        query = query.filter(Confirmation.improvement_id == improvement_id)
    if confirmer_id:
        query = query.filter(Confirmation.confirmer_id == confirmer_id)
    if status:
        query = query.filter(Confirmation.status == status)
    
    # Apply pagination
    query = query.order_by(Confirmation.created_at.desc())
    return query.offset(skip).limit(limit).all()

def get_confirmations_by_improvement(db: Session, improvement_id: int, skip: int = 0, limit: int = 100) -> List[Confirmation]:
    """Get all confirmations for a specific improvement"""
    return db.query(Confirmation).filter(
        Confirmation.improvement_id == improvement_id
    ).order_by(Confirmation.created_at.desc()).offset(skip).limit(limit).all()

def get_confirmations_by_confirmer(db: Session, confirmer_id: int, skip: int = 0, limit: int = 100) -> List[Confirmation]:
    """Get all confirmations submitted by a specific confirmer"""
    return db.query(Confirmation).filter(
        Confirmation.confirmer_id == confirmer_id
    ).order_by(Confirmation.created_at.desc()).offset(skip).limit(limit).all()

def create_confirmation(db: Session, confirmation: ConfirmationCreate) -> Confirmation:
    """Create a new confirmation"""
    db_confirmation = Confirmation(
        improvement_id=confirmation.improvement_id,
        confirmer_id=confirmation.confirmer_id,
        status=confirmation.status,
        comment=confirmation.comment,
        confirmation_date=confirmation.confirmation_date,
        created_at=datetime.utcnow()
    )
    db.add(db_confirmation)
    db.commit()
    db.refresh(db_confirmation)
    
    # Update defect status based on confirmation status
    if confirmation.status == "接受":
        # Get the defect_id from the improvement
        improvement = db.query(Improvement).filter(Improvement.improvement_id == confirmation.improvement_id).first()
        if improvement:
            defect = db.query(Defect).filter(Defect.defect_id == improvement.defect_id).first()
            if defect:
                defect.status = "已完成"
                db.commit()
    elif confirmation.status == "退回":
        # Get the defect_id from the improvement
        improvement = db.query(Improvement).filter(Improvement.improvement_id == confirmation.improvement_id).first()
        if improvement:
            defect = db.query(Defect).filter(Defect.defect_id == improvement.defect_id).first()
            if defect:
                defect.status = "改善中"
                db.commit()
    
    return db_confirmation

def update_confirmation(db: Session, confirmation_id: int, confirmation: ConfirmationUpdate) -> Optional[Confirmation]:
    """Update an existing confirmation"""
    db_confirmation = get_confirmation(db, confirmation_id)
    if not db_confirmation:
        return None
    
    update_data = confirmation.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_confirmation, key, value)
    
    db.commit()
    db.refresh(db_confirmation)
    
    # Update defect status based on confirmation status if status was updated
    if "status" in update_data:
        if update_data["status"] == "接受":
            # Get the defect_id from the improvement
            improvement = db.query(Improvement).filter(Improvement.improvement_id == db_confirmation.improvement_id).first()
            if improvement:
                defect = db.query(Defect).filter(Defect.defect_id == improvement.defect_id).first()
                if defect:
                    defect.status = "已完成"
                    db.commit()
        elif update_data["status"] == "退回":
            # Get the defect_id from the improvement
            improvement = db.query(Improvement).filter(Improvement.improvement_id == db_confirmation.improvement_id).first()
            if improvement:
                defect = db.query(Defect).filter(Defect.defect_id == improvement.defect_id).first()
                if defect:
                    defect.status = "改善中"
                    db.commit()
    
    return db_confirmation

def delete_confirmation(db: Session, confirmation_id: int) -> bool:
    """Delete a confirmation"""
    db_confirmation = get_confirmation(db, confirmation_id)
    if not db_confirmation:
        return False
    
    db.delete(db_confirmation)
    db.commit()
    return True

def get_confirmation_with_details(db: Session, confirmation_id: int) -> Optional[Dict[str, Any]]:
    """Get a confirmation with related details"""
    # Query the confirmation with related entities
    confirmation = (
        db.query(
            Confirmation,
            User.name.label("confirmer_name"),
            Improvement.content.label("improvement_content"),
            Defect.defect_description
        )
        .join(User, Confirmation.confirmer_id == User.user_id, isouter=True)
        .join(Improvement, Confirmation.improvement_id == Improvement.improvement_id)
        .join(Defect, Improvement.defect_id == Defect.defect_id)
        .filter(Confirmation.confirmation_id == confirmation_id)
        .first()
    )
    
    if not confirmation:
        return None
    
    confirmation_obj, confirmer_name, improvement_content, defect_description = confirmation
    
    # Create result dictionary
    result = {
        "confirmation_id": confirmation_obj.confirmation_id,
        "improvement_id": confirmation_obj.improvement_id,
        "improvement_content": improvement_content,
        "defect_description": defect_description,
        "confirmer_id": confirmation_obj.confirmer_id,
        "confirmer_name": confirmer_name,
        "confirmation_date": confirmation_obj.confirmation_date,
        "comment": confirmation_obj.comment,
        "status": confirmation_obj.status,
        "created_at": confirmation_obj.created_at
    }
    
    return result
