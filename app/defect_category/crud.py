from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Optional, Dict, Any

from app.defect_category.models import DefectCategory
from app.defect_category.schemas import DefectCategoryCreate, DefectCategoryUpdate
from app.defect.models import Defect

def get_defect_category(db: Session, defect_category_id: int) -> Optional[DefectCategory]:
    """Get a single defect category by ID"""
    return db.query(DefectCategory).filter(DefectCategory.defect_category_id == defect_category_id).first()

def get_defect_categories(db: Session, skip: int = 0, limit: int = 100) -> List[DefectCategory]:
    """Get a list of defect categories with pagination"""
    return db.query(DefectCategory).offset(skip).limit(limit).all()

def create_defect_category(db: Session, defect_category: DefectCategoryCreate) -> DefectCategory:
    """Create a new defect category"""
    db_defect_category = DefectCategory(
        category_name=defect_category.category_name,
        project_id=defect_category.project_id,
        description=defect_category.description
    )
    db.add(db_defect_category)
    db.commit()
    db.refresh(db_defect_category)
    return db_defect_category

def update_defect_category(db: Session, defect_category_id: int, defect_category: DefectCategoryUpdate) -> Optional[DefectCategory]:
    """Update an existing defect category"""
    db_defect_category = get_defect_category(db, defect_category_id)
    if not db_defect_category:
        return None
    
    update_data = defect_category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_defect_category, key, value)
    
    db.commit()
    db.refresh(db_defect_category)
    return db_defect_category

def delete_defect_category(db: Session, defect_category_id: int) -> bool:
    """Delete a defect category"""
    db_defect_category = get_defect_category(db, defect_category_id)
    if not db_defect_category:
        return False
    
    db.delete(db_defect_category)
    db.commit()
    return True

def get_defect_categories_with_counts(db: Session) -> List[Dict[str, Any]]:
    """Get defect categories with defect counts"""
    categories = get_defect_categories(db)
    
    result = []
    for category in categories:
        # Count defects in this category
        defect_count = db.query(func.count(Defect.defect_id)).filter(
            Defect.defect_category_id == category.defect_category_id
        ).scalar()
        
        result.append({
            "defect_category_id": category.defect_category_id,
            "project_id": category.project_id,
            "category_name": category.category_name,
            "description": category.description,
            "defect_count": defect_count
        })
    
    return result
