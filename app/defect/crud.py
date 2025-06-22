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

def get_defect_by_unique_code(db: Session, unique_code: str) -> Optional[Defect]:
    """Get a single defect by unique code"""
    return db.query(Defect).filter(Defect.unique_code == unique_code).first()

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
    # 使用 joinedload 一次性載入關聯資料
    query = db.query(Defect)\
        .options(
            joinedload(Defect.project),
            joinedload(Defect.submitter),
            joinedload(Defect.category),
            joinedload(Defect.assigned_vendor),
            joinedload(Defect.responsible_vendor)
        )
    
    # 套用過濾條件
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
    
    # 套用分頁
    defects = query.offset(skip).limit(limit).all()
    
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
            "created_at": defect.created_at,
            
            # 直接從關聯資料中獲取名稱
            "project_name": defect.project.project_name if defect.project else None,
            "submitter_name": defect.submitter.name if defect.submitter else None,
            "category_name": defect.category.category_name if defect.category else None,
            "assigned_vendor_name": defect.assigned_vendor.vendor_name if defect.assigned_vendor else None,
            "responsible_vendor_name": defect.responsible_vendor.vendor_name if defect.responsible_vendor else None
        }
        
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

def get_defect_details(
    db: Session,
    defect_id: int,
    with_marks: bool = False,
    with_photos: bool = False,
    with_improvements: bool = False,
    with_full_related: bool = False
    ) -> Optional[Dict[str, Any]]:
    """Get a defect with related details"""
    # 使用 aliased 來處理相同表格的多次 join
    # 決定 joinedload 深度
    options = [
        joinedload(Defect.project),
        joinedload(Defect.submitter),
        joinedload(Defect.category),
        joinedload(Defect.assigned_vendor),
        joinedload(Defect.responsible_vendor)
    ]
    if with_marks:
        options.append(joinedload(Defect.defect_marks))
    if with_improvements:
        options.append(joinedload(Defect.improvements))

    defect_obj = db.query(Defect).filter(Defect.defect_id == defect_id).options(*options).first()
    if not defect_obj:
        return None

    # 基本資料
    defect_data = {
        "defect_id": defect_obj.defect_id,
        "unique_code": defect_obj.unique_code,
        "project_id": defect_obj.project_id,
        "submitted_id": defect_obj.submitted_id,
        "location": defect_obj.location,
        "defect_category_id": defect_obj.defect_category_id,
        "defect_description": defect_obj.defect_description,
        "assigned_vendor_id": defect_obj.assigned_vendor_id,
        "repair_description": defect_obj.repair_description,
        "expected_completion_day": defect_obj.expected_completion_day,
        "responsible_vendor_id": defect_obj.responsible_vendor_id,
        "previous_defect_id": defect_obj.previous_defect_id,
        "status": defect_obj.status,
        "created_at": defect_obj.created_at,
        "confirmer_id": defect_obj.confirmer_id,
        "project_name": defect_obj.project.project_name if defect_obj.project else None,
        "submitter_name": defect_obj.submitter.name if defect_obj.submitter else None,
        "category_name": defect_obj.category.category_name if defect_obj.category else None,
        "assigned_vendor_name": defect_obj.assigned_vendor.vendor_name if defect_obj.assigned_vendor else None,
        "responsible_vendor_name": defect_obj.responsible_vendor.vendor_name if defect_obj.responsible_vendor else None
    }

    # 標記
    if with_marks:
        defect_data["defect_marks"] = [
            {
                "defect_mark_id": mark.defect_mark_id,
                "defect_id": mark.defect_id,
                "base_map_id": mark.base_map_id,
                "coordinate_x": mark.coordinate_x,
                "coordinate_y": mark.coordinate_y,
                "scale": mark.scale
            } for mark in defect_obj.defect_marks
        ]
    # 照片
    if with_photos:
        photos = (
            db.query(Photo)
            .filter(Photo.related_type == "defect")
            .filter(Photo.related_id == defect_id)
            .all()
        )
        defect_data["photos"] = [
            {
                "photo_id": photo.photo_id,
                "related_type": photo.related_type,
                "related_id": photo.related_id,
                "description": photo.description,
                "image_url": photo.image_url,
                "created_at": photo.created_at
            } for photo in photos
        ]
    # 改善
    if with_improvements:
        defect_data["improvements"] = [
            {
                "improvement_id": improvement.improvement_id,
                "defect_id": improvement.defect_id,
                "submitter_id": improvement.submitter_id,
                "content": improvement.content,
                "improvement_date": improvement.improvement_date,
                "created_at": improvement.created_at
            } for improvement in defect_obj.improvements
        ]
    # 完整關聯
    if with_full_related:
        if defect_obj.category:
            defect_data["defect_category"] = {
                "defect_category_id": defect_obj.category.defect_category_id,
                "category_name": defect_obj.category.category_name,
                "description": defect_obj.category.description
            }
        if defect_obj.assigned_vendor:
            defect_data["assigned_vendor"] = {
                "vendor_id": defect_obj.assigned_vendor.vendor_id,
                "vendor_name": defect_obj.assigned_vendor.vendor_name,
                "contact_person": defect_obj.assigned_vendor.contact_person,
                "phone": defect_obj.assigned_vendor.phone,
                "email": defect_obj.assigned_vendor.email,
                "responsibilities": defect_obj.assigned_vendor.responsibilities
            }
        if defect_obj.responsible_vendor:
            defect_data["responsible_vendor"] = {
                "vendor_id": defect_obj.responsible_vendor.vendor_id,
                "vendor_name": defect_obj.responsible_vendor.vendor_name,
                "contact_person": defect_obj.responsible_vendor.contact_person,
                "phone": defect_obj.responsible_vendor.phone,
                "email": defect_obj.responsible_vendor.email,
                "responsibilities": defect_obj.responsible_vendor.responsibilities
            }
        if defect_obj.submitter:
            defect_data["submitter"] = {
                "user_id": defect_obj.submitter.user_id,
                "name": defect_obj.submitter.name,
                "email": defect_obj.submitter.email,
                "line_id": defect_obj.submitter.line_id,
                "company_name": defect_obj.submitter.company_name
            }
        if defect_obj.project:
            defect_data["project"] = {
                "project_id": defect_obj.project.project_id,
                "project_name": defect_obj.project.project_name,
                "image_path": defect_obj.project.image_path,
                "created_at": defect_obj.project.created_at
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
