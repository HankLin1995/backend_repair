from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import Base, engine

# Import routers
from app.project.routers import router as project_router
from app.user.routers import router as user_router
from app.permission.routers import router as permission_router
from app.base_map.routers import router as base_map_router
from app.vendor.routers import router as vendor_router
from app.defect_category.routers import router as defect_category_router
from app.defect.routers import router as defect_router
from app.defect_mark.routers import router as defect_mark_router
from app.photo.routers import router as photo_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Backend Defect API",
    description="API for managing construction defects",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(project_router, prefix="/projects", tags=["Projects"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(permission_router, prefix="/permissions", tags=["Permissions"])
app.include_router(base_map_router, prefix="/base-maps", tags=["Base Maps"])
app.include_router(vendor_router, prefix="/vendors", tags=["Vendors"])
app.include_router(defect_category_router, prefix="/defect-categories", tags=["Defect Categories"])
app.include_router(defect_router, prefix="/defects", tags=["Defects"])
app.include_router(defect_mark_router, prefix="/defect-marks", tags=["Defect Marks"])
app.include_router(photo_router, prefix="/photos", tags=["Photos"])

# Mount static files directory for photos
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    return {"message": "Backend Defect API"}
