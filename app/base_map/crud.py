from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Optional, Dict, Any
import os

from app.base_map.models import BaseMap
from app.base_map.schemas import BaseMapCreate, BaseMapUpdate
from app.defect_mark.models import DefectMark

def get_base_map(db: Session, base_map_id: int) -> Optional[BaseMap]:
    """Get a single base map by ID"""
    return db.query(BaseMap).filter(BaseMap.base_map_id == base_map_id).first()

def get_base_maps(db: Session, skip: int = 0, limit: int = 100) -> List[BaseMap]:
    """Get a list of base maps with pagination"""
    return db.query(BaseMap).offset(skip).limit(limit).all()

def get_base_maps_by_project(db: Session, project_id: int) -> List[BaseMap]:
    """Get all base maps for a specific project"""
    return db.query(BaseMap).filter(BaseMap.project_id == project_id).all()

def create_base_map(db: Session, base_map: BaseMapCreate) -> BaseMap:
    """Create a new base map"""
    db_base_map = BaseMap(
        project_id=base_map.project_id,
        map_name=base_map.map_name,
        file_path=base_map.file_path
    )
    db.add(db_base_map)
    db.commit()
    db.refresh(db_base_map)
    return db_base_map

def update_base_map(db: Session, base_map_id: int, base_map: BaseMapUpdate) -> Optional[BaseMap]:
    """Update an existing base map"""
    db_base_map = get_base_map(db, base_map_id)
    if not db_base_map:
        return None
    
    update_data = base_map.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_base_map, key, value)
    
    db.commit()
    db.refresh(db_base_map)
    return db_base_map

def delete_base_map(db: Session, base_map_id: int) -> bool:
    """Delete a base map"""
    db_base_map = get_base_map(db, base_map_id)
    if not db_base_map:
        return False

    # 刪除圖片檔案（若不是 default.png）
    if db_base_map.file_path and os.path.exists(db_base_map.file_path):
        try:
            os.remove(db_base_map.file_path)
        except Exception:
            pass
    
    db.delete(db_base_map)
    db.commit()
    return True

def get_base_maps_with_defect_counts(db: Session, project_id: int) -> List[Dict[str, Any]]:
    """Get base maps with defect counts for a project"""
    base_maps = get_base_maps_by_project(db, project_id)
    
    result = []
    for base_map in base_maps:
        # Count defect marks for this base map
        defect_count = db.query(func.count(DefectMark.defect_mark_id)).filter(
            DefectMark.base_map_id == base_map.base_map_id
        ).scalar()
        
        result.append({
            "base_map_id": base_map.base_map_id,
            "project_id": base_map.project_id,
            "map_name": base_map.map_name,
            "file_path": base_map.file_path,
            "defect_count": defect_count
        })
    
    return result
