from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.user.models import User
from app.user.schemas import UserCreate, UserUpdate
from app.permission.models import Permission
from app.project.models import Project

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get a single user by ID"""
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_line_id(db: Session, line_id: str) -> Optional[User]:
    """Get a single user by LINE ID"""
    return db.query(User).filter(User.line_id == line_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a single user by email"""
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get a list of users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    db_user = User(
        name=user.name,
        email=user.email,
        company_name=user.company_name,
        line_id=user.line_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
    """Update an existing user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

def get_user_with_projects(db: Session, user_id: int) -> Optional[Dict[str, Any]]:
    """Get a user with their projects and roles"""
    user = get_user(db, user_id)
    if not user:
        return None
    
    # Get user's projects and roles
    projects_query = (
        db.query(Project, Permission.user_role)
        .join(Permission, Permission.project_id == Project.project_id)
        .join(User, User.email == Permission.user_email)
        .filter(User.user_id == user_id)
    )
    
    projects_data = []
    for project, role in projects_query:
        projects_data.append({
            "project_id": project.project_id,
            "project_name": project.project_name,
            "role": role
        })
    
    # Create result dictionary
    result = {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "company_name": user.company_name,
        "line_id": user.line_id,
        "created_at": user.created_at,
        "projects": projects_data
    }
    
    return result
