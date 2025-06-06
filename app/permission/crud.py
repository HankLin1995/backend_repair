from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.permission.models import Permission
from app.permission.schemas import PermissionCreate, PermissionUpdate
from app.project.models import Project
from app.user.models import User

def get_permission(db: Session, permission_id: int) -> Optional[Permission]:
    """Get a single permission by ID"""
    return db.query(Permission).filter(Permission.permission_id == permission_id).first()

def get_permissions(db: Session, skip: int = 0, limit: int = 100) -> List[Permission]:
    """Get a list of permissions with pagination"""
    return db.query(Permission).offset(skip).limit(limit).all()

def get_permissions_by_project(db: Session, project_id: int) -> List[Permission]:
    """Get all permissions for a specific project"""
    return db.query(Permission).filter(Permission.project_id == project_id).all()

def get_permissions_by_user(db: Session, user_email: str) -> List[Permission]:
    """Get all permissions for a specific user"""
    return db.query(Permission).filter(Permission.user_email == user_email).all()

def create_permission(db: Session, permission: PermissionCreate) -> Permission:
    """Create a new permission"""
    # Check if permission already exists
    existing = (
        db.query(Permission)
        .filter(
            Permission.project_id == permission.project_id,
            Permission.user_email == permission.user_email
        )
        .first()
    )
    
    if existing:
        # Update existing permission
        existing.user_role = permission.user_role
        db.commit()
        db.refresh(existing)
        return existing
    
    # Create new permission
    db_permission = Permission(
        project_id=permission.project_id,
        user_email=permission.user_email,
        user_role=permission.user_role
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def update_permission(db: Session, permission_id: int, permission: PermissionUpdate) -> Optional[Permission]:
    """Update an existing permission"""
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        return None
    
    # 保存原始 project_id
    original_project_id = db_permission.project_id
    
    update_data = permission.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_permission, key, value)
    
    # 確保 project_id 不會被設為 None
    if db_permission.project_id is None:
        db_permission.project_id = original_project_id
    
    db.commit()
    db.refresh(db_permission)
    return db_permission

def delete_permission(db: Session, permission_id: int) -> bool:
    """Delete a permission"""
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        return False
    
    db.delete(db_permission)
    db.commit()
    return True

def get_permissions_with_details(db: Session, project_id: Optional[int] = None, user_email: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get permissions with project and user details"""
    # 使用顯式連接而不是依賴外鍵關係
    query = (
        db.query(
            Permission,
            Project.project_name,
            User.name.label("user_name"),
            User.avatar_path
        )
        .join(Project, Permission.project_id == Project.project_id)
        # 使用顯式條件連接 User 表格
        .outerjoin(User, Permission.user_email == User.email)
    )
    
    if project_id:
        query = query.filter(Permission.project_id == project_id)
    
    if user_email:
        query = query.filter(Permission.user_email == user_email)
    
    results = []
    for permission, project_name, user_name, avatar_path in query:
        results.append({
            "permission_id": permission.permission_id,
            "project_id": permission.project_id,
            "user_email": permission.user_email,
            "user_role": permission.user_role,
            "project_name": project_name,
            "user_name": user_name if user_name is not None else "",
            "avatar_path": avatar_path if avatar_path is not None else "static/avatar/default.png"
        })
    
    return results
