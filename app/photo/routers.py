from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
import uuid
from datetime import datetime

from app.database import get_db
from app.photo import crud, schemas
from app.utils import check_exists
from app.defect.models import Defect
from app.improvement.models import Improvement
from app.confirmation.models import Confirmation

router = APIRouter()

# @router.post("/", response_model=schemas.PhotoResponse, status_code=status.HTTP_201_CREATED)
# def create_photo(photo: schemas.PhotoCreate, request: Request, db: Session = Depends(get_db)):
#     """Create a new photo (manual entry with URL)"""
#     # Check if related item exists based on related_type
#     if photo.related_type == "defect":
#         check_exists(db, Defect, photo.related_id, "defect_id")
#     elif photo.related_type == "improvement":
#         check_exists(db, Improvement, photo.related_id, "improvement_id")
#     elif photo.related_type == "confirmation":
#         check_exists(db, Confirmation, photo.related_id, "confirmation_id")
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Invalid related_type: {photo.related_type}. Must be one of: 'defect', 'improvement', 'confirmation'"
#         )
    
#     db_photo = crud.create_photo(db=db, photo=photo)
    
#     # Add full URL to the photo
#     base_url = str(request.base_url).rstrip('/')
#     full_url = f"{base_url}{db_photo.image_url}"
    
#     return schemas.PhotoResponse(
#         **db_photo.__dict__,
#         full_url=full_url
#     )

@router.post("/", response_model=schemas.PhotoResponse, status_code=status.HTTP_201_CREATED)
async def upload_photo(
    request: Request,
    file: UploadFile = File(...),
    related_type: str = Form(...),
    related_id: int = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload a new photo file"""
    # Check if related item exists based on related_type
    if related_type == "defect":
        check_exists(db, Defect, related_id, "defect_id")
    elif related_type == "improvement":
        check_exists(db, Improvement, related_id, "improvement_id")
    elif related_type == "confirmation":
        check_exists(db, Confirmation, related_id, "confirmation_id")
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid related_type: {related_type}. Must be one of: 'defect', 'improvement', 'confirmation'"
        )
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1].lower()
    allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Create organized directory structure based on related_type
    # 使用專案根目錄，確保在 Docker 容器中也能正確掛載
    project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".."))
    photos_dir = os.path.join(project_root, "static", "photos", related_type)
    os.makedirs(photos_dir, exist_ok=True)
    
    # Create unique filename with related_type, related_id, timestamp and short UUID
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    short_uuid = uuid.uuid4().hex[:8]  # 使用較短的 UUID 保持檔名簡潔
    unique_filename = f"{related_type}_{related_id}_{timestamp}_{short_uuid}{file_extension}"
    
    # Save file to disk
    file_path = os.path.join(photos_dir, unique_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create relative URL path for database
    relative_url = f"/static/photos/{related_type}/{unique_filename}"
    
    # Create photo record in database
    photo_data = schemas.PhotoCreate(
        related_type=related_type,
        related_id=related_id,
        description=description,
        image_url=relative_url
    )
    
    db_photo = crud.create_photo(db=db, photo=photo_data)
    
    # Generate full URL for response
    base_url = str(request.base_url).rstrip('/')
    full_url = f"{base_url}{relative_url}"
    
    # Create response with full URL
    response_data = schemas.PhotoResponse(
        **db_photo.__dict__,
        full_url=full_url
    )
    
    return response_data

@router.get("/", response_model=List[schemas.PhotoResponse])
def read_photos(
    request: Request,
    related_type: Optional[str] = None,
    related_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get a list of photos with pagination and optional filtering"""
    if related_type and related_id:
        # Validate related_type
        if related_type not in ["defect", "improvement", "confirmation"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid related_type: {related_type}. Must be one of: 'defect', 'improvement', 'confirmation'"
            )
        
        # Check if related item exists
        if related_type == "defect":
            check_exists(db, Defect, related_id, "defect_id")
        elif related_type == "improvement":
            check_exists(db, Improvement, related_id, "improvement_id")
        elif related_type == "confirmation":
            check_exists(db, Confirmation, related_id, "confirmation_id")
        
        # Get photos for the related item
        photos = crud.get_photos_by_related(db, related_type=related_type, related_id=related_id)
    else:
        photos = crud.get_photos(db, skip=skip, limit=limit)
    
    # Add full URL to each photo
    base_url = str(request.base_url).rstrip('/')
    result = []
    for photo in photos:
        full_url = f"{base_url}{photo.image_url}"
        result.append(schemas.PhotoResponse(
            **photo.__dict__,
            full_url=full_url
        ))
    
    return result

@router.get("/{photo_id}", response_model=schemas.PhotoResponse)
def read_photo(photo_id: int, request: Request, db: Session = Depends(get_db)):
    """Get a specific photo by ID"""
    db_photo = crud.get_photo(db, photo_id=photo_id)
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    # Add full URL to the photo
    base_url = str(request.base_url).rstrip('/')
    full_url = f"{base_url}{db_photo.image_url}"
    
    return schemas.PhotoResponse(
        **db_photo.__dict__,
        full_url=full_url
    )

@router.put("/{photo_id}", response_model=schemas.PhotoResponse)
def update_photo(
    photo_id: int, photo: schemas.PhotoUpdate, request: Request, db: Session = Depends(get_db)
):
    """Update a photo"""
    db_photo = crud.update_photo(db, photo_id=photo_id, photo=photo)
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    # Add full URL to the photo
    base_url = str(request.base_url).rstrip('/')
    full_url = f"{base_url}{db_photo.image_url}"
    
    return schemas.PhotoResponse(
        **db_photo.__dict__,
        full_url=full_url
    )

@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    """Delete a photo"""
    success = crud.delete_photo(db, photo_id=photo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Photo not found")
    return None
