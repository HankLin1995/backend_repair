from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.defect_mark.models import DefectMark
from app.defect_mark.schemas import DefectMarkCreate, DefectMarkUpdate
from app.defect.models import Defect
from app.base_map.models import BaseMap

def get_defect_mark(db: Session, defect_mark_id: int) -> Optional[DefectMark]:
    """Get a single defect mark by ID"""
    return db.query(DefectMark).filter(DefectMark.defect_mark_id == defect_mark_id).first()

def get_defect_marks(db: Session, skip: int = 0, limit: int = 100) -> List[DefectMark]:
    """Get a list of defect marks with pagination"""
    return db.query(DefectMark).offset(skip).limit(limit).all()

def get_defect_marks_by_defect(db: Session, defect_id: int) -> List[DefectMark]:
    """Get all defect marks for a specific defect"""
    return db.query(DefectMark).filter(DefectMark.defect_form_id == defect_id).all()

def get_defect_marks_by_base_map(db: Session, base_map_id: int) -> List[DefectMark]:
    """Get all defect marks for a specific base map"""
    return db.query(DefectMark).filter(DefectMark.base_map_id == base_map_id).all()

def create_defect_mark(db: Session, defect_mark: DefectMarkCreate) -> DefectMark:
    """Create a new defect mark"""
    db_defect_mark = DefectMark(
        defect_form_id=defect_mark.defect_form_id,
        base_map_id=defect_mark.base_map_id,
        coordinate_x=defect_mark.coordinate_x,
        coordinate_y=defect_mark.coordinate_y,
        scale=defect_mark.scale
    )
    db.add(db_defect_mark)
    db.commit()
    db.refresh(db_defect_mark)
    return db_defect_mark

def update_defect_mark(db: Session, defect_mark_id: int, defect_mark: DefectMarkUpdate) -> Optional[DefectMark]:
    """Update an existing defect mark"""
    db_defect_mark = get_defect_mark(db, defect_mark_id)
    if not db_defect_mark:
        return None
    
    update_data = defect_mark.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_defect_mark, key, value)
    
    db.commit()
    db.refresh(db_defect_mark)
    return db_defect_mark

def delete_defect_mark(db: Session, defect_mark_id: int) -> bool:
    """Delete a defect mark"""
    db_defect_mark = get_defect_mark(db, defect_mark_id)
    if not db_defect_mark:
        return False
    
    db.delete(db_defect_mark)
    db.commit()
    return True

def get_defect_marks_with_details(db: Session, base_map_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get defect marks with defect and base map details"""
    query = (
        db.query(
            DefectMark,
            Defect.defect_description,
            BaseMap.map_name
        )
        .join(Defect, DefectMark.defect_form_id == Defect.defect_id)
        .join(BaseMap, DefectMark.base_map_id == BaseMap.base_map_id)
    )
    
    if base_map_id:
        query = query.filter(DefectMark.base_map_id == base_map_id)
    
    results = []
    for defect_mark, defect_description, map_name in query:
        results.append({
            "defect_mark_id": defect_mark.defect_mark_id,
            "defect_form_id": defect_mark.defect_form_id,
            "base_map_id": defect_mark.base_map_id,
            "coordinate_x": defect_mark.coordinate_x,
            "coordinate_y": defect_mark.coordinate_y,
            "scale": defect_mark.scale,
            "defect_description": defect_description,
            "map_name": map_name
        })
    
    return results
