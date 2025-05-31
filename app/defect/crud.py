from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.defect.models import Defect
from app.defect.schemas import DefectCreate, DefectUpdate
from app.project.models import Project
from app.user.models import User
from app.defect_category.models import DefectCategory
from app.vendor.models import Vendor
from app.defect_mark.models import DefectMark
from app.photo.models import Photo

def get_defect(db: Session, defect_id: int) -> Optional[Defect]:
    """Get a single defect by ID"""
    return db.query(Defect).filter(Defect.defect_id == defect_id).first()

def get_defects(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    project_id: Optional[int] = None,
    submitted_id: Optional[int] = None,
    defect_category_id: Optional[int] = None,
    assigned_vendor_id: Optional[int] = None,
    confirmation_status: Optional[str] = None
) -> List[Defect]:
    """Get a list of defects with pagination and optional filtering"""
    query = db.query(Defect)
    
    # Apply filters if provided
    if project_id:
        query = query.filter(Defect.project_id == project_id)
    if submitted_id:
        query = query.filter(Defect.submitted_id == submitted_id)
    if defect_category_id:
        query = query.filter(Defect.defect_category_id == defect_category_id)
    if assigned_vendor_id:
        query = query.filter(Defect.assigned_vendor_id == assigned_vendor_id)
    if confirmation_status:
        query = query.filter(Defect.confirmation_status == confirmation_status)
    
    # Apply pagination
    query = query.order_by(Defect.created_at.desc())
    return query.offset(skip).limit(limit).all()

def create_defect(db: Session, defect: DefectCreate) -> Defect:
    """Create a new defect"""
    db_defect = Defect(
        project_id=defect.project_id,
        submitted_id=defect.submitted_id,
        defect_category_id=defect.defect_category_id,
        defect_description=defect.defect_description,
        assigned_vendor_id=defect.assigned_vendor_id,
        repair_description=defect.repair_description,
        expected_completion_date=defect.expected_completion_date,
        repair_completed_at=defect.repair_completed_at,
        confirmation_status=defect.confirmation_status or "pending",
        confirmation_time=defect.confirmation_time,
        confirmer_id=defect.confirmer_id
    )
    db.add(db_defect)
    db.commit()
    db.refresh(db_defect)
    return db_defect

def update_defect(db: Session, defect_id: int, defect: DefectUpdate) -> Optional[Defect]:
    """Update an existing defect"""
    db_defect = get_defect(db, defect_id)
    if not db_defect:
        return None
    
    update_data = defect.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_defect, key, value)
    
    # Update the updated_at timestamp
    db_defect.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_defect)
    return db_defect

def delete_defect(db: Session, defect_id: int) -> bool:
    """Delete a defect"""
    db_defect = get_defect(db, defect_id)
    if not db_defect:
        return False
    
    db.delete(db_defect)
    db.commit()
    return True

def get_defect_with_details(db: Session, defect_id: int) -> Optional[Dict[str, Any]]:
    """Get a defect with related details"""
    # 使用 aliased 來處理相同表格的多次 join
    from sqlalchemy.orm import aliased
    SubmitterUser = aliased(User)
    ConfirmerUser = aliased(User)
    
    # Query the defect with all related entities
    defect = (
        db.query(
            Defect,
            Project.project_name,
            SubmitterUser.name.label("submitter_name"),
            DefectCategory.category_name,
            Vendor.vendor_name,
            ConfirmerUser.name.label("confirmer_name")
        )
        .join(Project, Defect.project_id == Project.project_id)
        .join(SubmitterUser, Defect.submitted_id == SubmitterUser.user_id, isouter=True)
        .join(DefectCategory, Defect.defect_category_id == DefectCategory.defect_category_id, isouter=True)
        .join(Vendor, Defect.assigned_vendor_id == Vendor.vendor_id, isouter=True)
        .outerjoin(ConfirmerUser, Defect.confirmer_id == ConfirmerUser.user_id)
        .filter(Defect.defect_id == defect_id)
        .first()
    )
    
    if not defect:
        return None
    
    defect_obj, project_name, submitter_name, category_name, vendor_name, confirmer_name = defect
    
    # Create result dictionary
    result = {
        "defect_id": defect_obj.defect_id,
        "project_id": defect_obj.project_id,
        "project_name": project_name,
        "submitted_id": defect_obj.submitted_id,
        "submitter_name": submitter_name,
        "defect_category_id": defect_obj.defect_category_id,
        "category_name": category_name,
        "defect_description": defect_obj.defect_description,
        "assigned_vendor_id": defect_obj.assigned_vendor_id,
        "vendor_name": vendor_name,
        "repair_description": defect_obj.repair_description,
        "expected_completion_date": defect_obj.expected_completion_date,
        "repair_completed_at": defect_obj.repair_completed_at,
        "confirmation_status": defect_obj.confirmation_status,
        "confirmation_time": defect_obj.confirmation_time,
        "confirmer_id": defect_obj.confirmer_id,
        "confirmer_name": confirmer_name,
        "created_at": defect_obj.created_at,
        "updated_at": defect_obj.updated_at
    }
    
    return result

def get_defect_with_marks_and_photos(db: Session, defect_id: int) -> Optional[Dict[str, Any]]:
    """Get a defect with related details, marks and photos"""
    # Get defect with basic details
    defect_data = get_defect_with_details(db, defect_id)
    if not defect_data:
        return None
    
    # Get defect marks
    defect_marks = (
        db.query(DefectMark)
        .filter(DefectMark.defect_form_id == defect_id)
        .all()
    )
    
    marks_data = []
    for mark in defect_marks:
        marks_data.append({
            "defect_mark_id": mark.defect_mark_id,
            "defect_form_id": mark.defect_form_id,
            "base_map_id": mark.base_map_id,
            "coordinate_x": mark.coordinate_x,
            "coordinate_y": mark.coordinate_y,
            "scale": mark.scale
        })
    
    # Get photos
    photos = (
        db.query(Photo)
        .filter(Photo.defect_form_id == defect_id)
        .all()
    )
    
    photos_data = []
    for photo in photos:
        photos_data.append({
            "photo_id": photo.photo_id,
            "defect_form_id": photo.defect_form_id,
            "description": photo.description,
            "photo_type": photo.photo_type,
            "image_url": photo.image_url,
            "created_at": photo.created_at
        })
    
    # Add marks and photos to result
    defect_data["defect_marks"] = marks_data
    defect_data["photos"] = photos_data
    
    return defect_data

def get_defect_stats(db: Session, project_id: Optional[int] = None) -> Dict[str, Any]:
    """Get defect statistics"""
    query = db.query(Defect)
    
    if project_id:
        query = query.filter(Defect.project_id == project_id)
    
    # Total defects
    total_count = query.count()
    
    # Count by status
    pending_count = query.filter(Defect.confirmation_status == "pending").count()
    in_progress_count = query.filter(Defect.confirmation_status == "in_progress").count()
    completed_count = query.filter(Defect.confirmation_status == "completed").count()
    
    # Count by category
    category_counts = (
        db.query(
            DefectCategory.category_name,
            func.count(Defect.defect_id).label("count")
        )
        .join(Defect, Defect.defect_category_id == DefectCategory.defect_category_id)
    )
    
    if project_id:
        category_counts = category_counts.filter(Defect.project_id == project_id)
    
    category_counts = category_counts.group_by(DefectCategory.category_name).all()
    
    category_stats = [{"category": name, "count": count} for name, count in category_counts]
    
    # Result
    return {
        "total_count": total_count,
        "pending_count": pending_count,
        "in_progress_count": in_progress_count,
        "completed_count": completed_count,
        "category_stats": category_stats
    }
