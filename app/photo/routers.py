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

router = APIRouter()

@router.post("/", response_model=schemas.PhotoResponse, status_code=status.HTTP_201_CREATED)
def create_photo(photo: schemas.PhotoCreate, request: Request, db: Session = Depends(get_db)):
    """Create a new photo (manual entry with URL)"""
    # Check if defect exists
    check_exists(db, Defect, photo.defect_form_id, "defect_id")
    
    db_photo = crud.create_photo(db=db, photo=photo)
    
    # Add full URL to the photo
    base_url = str(request.base_url).rstrip('/')
    full_url = f"{base_url}{db_photo.image_url}"
    
    return schemas.PhotoResponse(
        **db_photo.__dict__,
        full_url=full_url
    )

@router.post("/upload/", response_model=schemas.PhotoResponse, status_code=status.HTTP_201_CREATED)
async def upload_photo(
    request: Request,
    file: UploadFile = File(...),
    defect_form_id: int = Form(...),
    description: Optional[str] = Form(None),
    photo_type: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload a new photo file"""
    # Check if defect exists
    check_exists(db, Defect, defect_form_id, "defect_id")
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1].lower()
    allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Create unique filename with timestamp and UUID
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{timestamp}_{uuid.uuid4().hex}{file_extension}"
    
    # Ensure directory exists
    photos_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "photos")
    os.makedirs(photos_dir, exist_ok=True)
    
    # Save file to disk
    file_path = os.path.join(photos_dir, unique_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create relative URL path for database
    relative_url = f"/static/photos/{unique_filename}"
    
    # Create photo record in database
    photo_data = schemas.PhotoCreate(
        defect_form_id=defect_form_id,
        description=description,
        photo_type=photo_type,
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
    defect_id: Optional[int] = None,
    photo_type: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get a list of photos with pagination and optional filtering"""
    if defect_id:
        # Check if defect exists
        check_exists(db, Defect, defect_id, "defect_id")
        
        if photo_type:
            photos = crud.get_photos_by_type(db, defect_id=defect_id, photo_type=photo_type)
        else:
            photos = crud.get_photos_by_defect(db, defect_id=defect_id)
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
