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
    db_project = Project(
        project_name=project.project_name,
        image_path=project.image_path
    )
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

import os

def delete_project(db: Session, project_id: int) -> bool:
    """Delete a project (and its image file if only used by this project)"""
    db_project = get_project(db, project_id)
    if not db_project:
        return False

    image_path = db_project.image_path
    # 只考慮刪除 project_id 專屬的圖片
    if (
        image_path
        and image_path != "static/project/default.png"
        and f"project_{project_id}" in os.path.basename(image_path)
        and os.path.exists(image_path)
    ):
        # 檢查資料庫是否還有其他專案引用這個檔案
        from app.project.models import Project
        other = db.query(Project).filter(
            Project.image_path == image_path, Project.project_id != project_id
        ).first()
        if not other:
            try:
                os.remove(image_path)
            except Exception:
                pass

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

def get_project_with_users(db: Session, project_id: int) -> Optional[Dict[str, Any]]:
    """Get a project with users"""
    project = get_project(db, project_id)
    if not project:
        return None
    
    # Get project's users and roles
    users_query = (
        db.query(User, Permission.user_role)
        .join(Permission, Permission.project_id == Project.project_id)
        .join(User, User.email == Permission.user_email)
        .filter(Project.project_id == project_id)
    )
    
    users_data = []
    for user, role in users_query:
        users_data.append({
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "company_name": user.company_name,
            "line_id": user.line_id,
            "created_at": user.created_at,
            "role": role
        })
    
    # Create result dictionary
    result = {
        "project_id": project.project_id,
        "project_name": project.project_name,
        "created_at": project.created_at,
        "users": users_data
    }
    
    return result

def get_project_roles(db: Session, project_id: int) -> Optional[Dict[str, Any]]:
    """獲取專案中的使用者電子郵件和對應的角色"""
    project = get_project(db, project_id)
    if not project:
        return None
    
    # 獲取專案中的所有使用者電子郵件和對應的角色
    user_roles_query = (
        db.query(Permission.user_email, Permission.user_role)
        .filter(Permission.project_id == project_id)
        .all()
    )
    
    # 創建使用者角色列表
    user_roles = [
        {"email": email, "role": role}
        for email, role in user_roles_query
    ]
    
    # 創建結果字典
    result = {
        "project_id": project.project_id,
        "project_name": project.project_name,
        "user_roles": user_roles
    }
    
    return result