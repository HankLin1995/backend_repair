from sqlalchemy.orm import Session, joinedload, aliased
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
from app.improvement.models import Improvement

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
    responsible_vendor_id: Optional[int] = None,
    status: Optional[str] = None
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
    if responsible_vendor_id:
        query = query.filter(Defect.responsible_vendor_id == responsible_vendor_id)
    if status:
        query = query.filter(Defect.status == status)
    
    # Apply pagination
    # query = query.order_by(Defect.created_at.desc())
    return query.offset(skip).limit(limit).all()

def get_defects_with_details(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    project_id: Optional[int] = None,
    submitted_id: Optional[int] = None,
    defect_category_id: Optional[int] = None,
    assigned_vendor_id: Optional[int] = None,
    responsible_vendor_id: Optional[int] = None,
    status: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get a list of defects with details including category name and vendor name"""
    # 獲取基本的缺失列表
    defects = get_defects(
        db, 
        skip=skip, 
        limit=limit,
        project_id=project_id,
        submitted_id=submitted_id,
        defect_category_id=defect_category_id,
        assigned_vendor_id=assigned_vendor_id,
        responsible_vendor_id=responsible_vendor_id,
        status=status
    )
    
    result = []
    for defect in defects:
        # 基本缺失資料
        defect_data = {
            "defect_id": defect.defect_id,
            "unique_code": defect.unique_code,
            "project_id": defect.project_id,
            "submitted_id": defect.submitted_id,
            "location": defect.location,
            "defect_category_id": defect.defect_category_id,
            "defect_description": defect.defect_description,
            "assigned_vendor_id": defect.assigned_vendor_id,
            "repair_description": defect.repair_description,
            "expected_completion_day": defect.expected_completion_day,
            "responsible_vendor_id": defect.responsible_vendor_id,
            "previous_defect_id": defect.previous_defect_id,
            "status": defect.status,
            "created_at": defect.created_at
        }
        
        # 獲取專案名稱
        project = db.query(Project).filter(Project.project_id == defect.project_id).first()
        if project:
            defect_data["project_name"] = project.project_name
        else:
            defect_data["project_name"] = None
        
        # 獲取提交者名稱
        submitter = db.query(User).filter(User.user_id == defect.submitted_id).first()
        if submitter:
            defect_data["submitter_name"] = submitter.name
        else:
            defect_data["submitter_name"] = None
        
        # 獲取分類名稱
        if defect.defect_category_id:
            category = db.query(DefectCategory).filter(
                DefectCategory.defect_category_id == defect.defect_category_id
            ).first()
            if category:
                defect_data["category_name"] = category.category_name
            else:
                defect_data["category_name"] = None
        else:
            defect_data["category_name"] = None
        
        # 獲取指派廠商名稱
        if defect.assigned_vendor_id:
            assigned_vendor = db.query(Vendor).filter(
                Vendor.vendor_id == defect.assigned_vendor_id
            ).first()
            if assigned_vendor:
                defect_data["assigned_vendor_name"] = assigned_vendor.vendor_name
            else:
                defect_data["assigned_vendor_name"] = None
        else:
            defect_data["assigned_vendor_name"] = None
        
        # 獲取負責廠商名稱
        if defect.responsible_vendor_id:
            responsible_vendor = db.query(Vendor).filter(
                Vendor.vendor_id == defect.responsible_vendor_id
            ).first()
            if responsible_vendor:
                defect_data["responsible_vendor_name"] = responsible_vendor.vendor_name
            else:
                defect_data["responsible_vendor_name"] = None
        else:
            defect_data["responsible_vendor_name"] = None
        
        result.append(defect_data)
    
    return result

def create_defect(db: Session, defect: DefectCreate) -> Defect:
    """Create a new defect"""
    db_defect = Defect(**defect.model_dump())
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
    SubmitterUser = aliased(User)
    AssignedVendor = aliased(Vendor)
    ResponsibleVendor = aliased(Vendor)
    
    # Query the defect with all related entities
    defect = (
        db.query(
            Defect,
            Project.project_name,
            SubmitterUser.name.label("submitter_name"),
            DefectCategory.category_name,
            AssignedVendor.vendor_name.label("assigned_vendor_name"),
            ResponsibleVendor.vendor_name.label("responsible_vendor_name")
        )
        .join(Project, Defect.project_id == Project.project_id)
        .join(SubmitterUser, Defect.submitted_id == SubmitterUser.user_id, isouter=True)
        .join(DefectCategory, Defect.defect_category_id == DefectCategory.defect_category_id, isouter=True)
        .join(AssignedVendor, Defect.assigned_vendor_id == AssignedVendor.vendor_id, isouter=True)
        .join(ResponsibleVendor, Defect.responsible_vendor_id == ResponsibleVendor.vendor_id, isouter=True)
        .filter(Defect.defect_id == defect_id)
        .first()
    )
    
    if not defect:
        return None
    
    defect_obj, project_name, submitter_name, category_name, assigned_vendor_name, responsible_vendor_name = defect
    
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
        "assigned_vendor_name": assigned_vendor_name,
        "responsible_vendor_id": defect_obj.responsible_vendor_id,
        "responsible_vendor_name": responsible_vendor_name,
        "repair_description": defect_obj.repair_description,
        "expected_completion_day": defect_obj.expected_completion_day,
        "previous_defect_id": defect_obj.previous_defect_id,
        "status": defect_obj.status,
        "created_at": defect_obj.created_at,
        "unique_code": defect_obj.unique_code,
        "location": defect_obj.location
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
        .filter(DefectMark.defect_id == defect_id)
        .all()
    )
    
    marks_data = []
    for mark in defect_marks:
        marks_data.append({
            "defect_mark_id": mark.defect_mark_id,
            "defect_id": mark.defect_id,
            "base_map_id": mark.base_map_id,
            "coordinate_x": mark.coordinate_x,
            "coordinate_y": mark.coordinate_y,
            "scale": mark.scale
        })
    
    # Get photos
    photos = (
        db.query(Photo)
        .filter(Photo.related_type == "defect")
        .filter(Photo.related_id == defect_id)
        .all()
    )
    
    photos_data = []
    for photo in photos:
        photos_data.append({
            "photo_id": photo.photo_id,
            "related_type": photo.related_type,
            "related_id": photo.related_id,
            "description": photo.description,
            "image_url": photo.image_url,
            "created_at": photo.created_at
        })
    
    # Get improvements
    improvements = (
        db.query(Improvement)
        .filter(Improvement.defect_id == defect_id)
        .all()
    )
    
    improvements_data = []
    for improvement in improvements:
        improvements_data.append({
            "improvement_id": improvement.improvement_id,
            "defect_id": improvement.defect_id,
            "submitter_id": improvement.submitter_id,
            "content": improvement.content,
            "improvement_date": improvement.improvement_date,
            "created_at": improvement.created_at
        })
    
    # Add marks, photos, and improvements to result
    defect_data["defect_marks"] = marks_data
    defect_data["photos"] = photos_data
    defect_data["improvements"] = improvements_data
    
    return defect_data

def get_defect_with_full_details(db: Session, defect_id: int) -> Optional[Dict[str, Any]]:
    """Get a defect with full details including related entities"""
    # 獲取基本的缺失資訊與相關實體
    defect_data = get_defect_with_marks_and_photos(db, defect_id)
    if not defect_data:
        return None
    
    # 獲取完整的 defect_category 資訊
    if defect_data.get("defect_category_id"):
        category = db.query(DefectCategory).filter(
            DefectCategory.defect_category_id == defect_data["defect_category_id"]
        ).first()
        if category:
            defect_data["defect_category"] = {
                "defect_category_id": category.defect_category_id,
                "category_name": category.category_name,
                "description": category.description
            }
    
    # 獲取完整的 assigned_vendor 資訊
    if defect_data.get("assigned_vendor_id"):
        assigned_vendor = db.query(Vendor).filter(
            Vendor.vendor_id == defect_data["assigned_vendor_id"]
        ).first()
        if assigned_vendor:
            defect_data["assigned_vendor"] = {
                "vendor_id": assigned_vendor.vendor_id,
                "vendor_name": assigned_vendor.vendor_name,
                "contact_person": assigned_vendor.contact_person,
                "phone": assigned_vendor.phone,
                "email": assigned_vendor.email,
                "responsibilities": assigned_vendor.responsibilities
            }
    
    # 獲取完整的 responsible_vendor 資訊
    if defect_data.get("responsible_vendor_id"):
        responsible_vendor = db.query(Vendor).filter(
            Vendor.vendor_id == defect_data["responsible_vendor_id"]
        ).first()
        if responsible_vendor:
            defect_data["responsible_vendor"] = {
                "vendor_id": responsible_vendor.vendor_id,
                "vendor_name": responsible_vendor.vendor_name,
                "contact_person": responsible_vendor.contact_person,
                "phone": responsible_vendor.phone,
                "email": responsible_vendor.email,
                "responsibilities": responsible_vendor.responsibilities
            }
    
    # 獲取完整的 submitter 資訊
    if defect_data.get("submitted_id"):
        submitter = db.query(User).filter(
            User.user_id == defect_data["submitted_id"]
        ).first()
        if submitter:
            defect_data["submitter"] = {
                "user_id": submitter.user_id,
                "name": submitter.name,
                "email": submitter.email,
                "line_id": submitter.line_id,
                "company_name": submitter.company_name
            }
    
    # 獲取完整的 confirmer 資訊
    if defect_data.get("confirmer_id"):
        confirmer = db.query(User).filter(
            User.user_id == defect_data["confirmer_id"]
        ).first()
        if confirmer:
            defect_data["confirmer"] = {
                "user_id": confirmer.user_id,
                "name": confirmer.name,
                "email": confirmer.email,
                "line_id": confirmer.line_id,
                "company_name": confirmer.company_name
            }
    
    # 獲取完整的 project 資訊
    if defect_data.get("project_id"):
        project = db.query(Project).filter(
            Project.project_id == defect_data["project_id"]
        ).first()
        if project:
            defect_data["project"] = {
                "project_id": project.project_id,
                "project_name": project.project_name,
                "image_path": project.image_path,
                "created_at": project.created_at
            }
    
    return defect_data

def get_defect_stats(db: Session, project_id: Optional[int] = None) -> Dict[str, Any]:
    """Get defect statistics"""
    query = db.query(Defect)
    
    if project_id:
        query = query.filter(Defect.project_id == project_id)
    
    # Total defects
    total_count = query.count()
    
    # Count by status
    waiting_count = query.filter(Defect.status == "等待中").count()
    improving_count = query.filter(Defect.status == "改善中").count()
    pending_confirmation_count = query.filter(Defect.status == "待確認").count()
    completed_count = query.filter(Defect.status == "已完成").count()
    rejected_count = query.filter(Defect.status == "退件").count()
    
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
        "waiting_count": waiting_count,
        "improving_count": improving_count,
        "pending_confirmation_count": pending_confirmation_count,
        "completed_count": completed_count,
        "rejected_count": rejected_count,
        "category_stats": category_stats
    }
