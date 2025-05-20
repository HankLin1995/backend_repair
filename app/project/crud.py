from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Optional, Dict, Any

from app.project.models import Project
from app.project.schemas import ProjectCreate, ProjectUpdate
from app.permission.models import Permission
from app.base_map.models import BaseMap
from app.defect.models import Defect

def get_project(db: Session, project_id: int) -> Optional[Project]:
    """Get a single project by ID"""
    return db.query(Project).filter(Project.project_id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    """Get a list of projects with pagination"""
    return db.query(Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: ProjectCreate) -> Project:
    """Create a new project"""
    db_project = Project(project_name=project.project_name)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project: ProjectUpdate) -> Optional[Project]:
    """Update an existing project"""
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    update_data = project.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int) -> bool:
    """Delete a project"""
    db_project = get_project(db, project_id)
    if not db_project:
        return False
    
    db.delete(db_project)
    db.commit()
    return True

def get_project_with_counts(db: Session, project_id: int) -> Optional[Dict[str, Any]]:
    """Get a project with counts of related entities"""
    project = get_project(db, project_id)
    if not project:
        return None
    
    # Count related entities
    base_map_count = db.query(func.count(BaseMap.base_map_id)).filter(BaseMap.project_id == project_id).scalar()
    defect_count = db.query(func.count(Defect.defect_id)).filter(Defect.project_id == project_id).scalar()
    user_count = db.query(func.count(Permission.permission_id)).filter(Permission.project_id == project_id).scalar()
    
    # Create result dictionary
    result = {
        "project_id": project.project_id,
        "project_name": project.project_name,
        "created_at": project.created_at,
        "base_map_count": base_map_count,
        "defect_count": defect_count,
        "user_count": user_count
    }
    
    return result
