import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import os
import sys
from datetime import datetime
from datetime import timedelta

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import Base, get_db
from app.main import app

# Use an in-memory SQLite database for testing
# 使用 SQLite 記憶體資料庫，速度極快
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 創建資料表 - 在測試開始前執行一次
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    # 每個測試使用獨立的資料庫連線
    connection = engine.connect()
    # 開始交易 - 這樣可以在測試結束後回滾，不影響其他測試
    transaction = connection.begin()
    
    # 創建一個綁定到當前連線的 session
    session = TestingSessionLocal(bind=connection)
    
    try:
        yield session
    finally:
        # 回滾交易，清除所有測試資料但保留表結構
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(db):
    # Override the get_db dependency to use the test database
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    # Remove the override after the test
    app.dependency_overrides.clear()

# Test data fixtures
@pytest.fixture
def test_project(db):
    from app.project.models import Project
    
    project = Project(
        project_name="Test Project",
        created_at=datetime.utcnow()
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@pytest.fixture
def test_user(db):
    from app.user.models import User
    
    user = User(
        name="Test User",
        line_id="test_line_id",
        email="test@example.com",
        company_name="Test Company",
        avatar_path="static/avatar/default.png",
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_permission(db, test_project, test_user):
    from app.permission.models import Permission
    
    permission = Permission(
        project_id=test_project.project_id,
        user_email=test_user.email,
        user_role="admin"
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

@pytest.fixture
def test_base_map(db, test_project):
    from app.base_map.models import BaseMap
    
    base_map = BaseMap(
        project_id=test_project.project_id,
        map_name="Test Base Map",
        file_path="/path/to/map.jpg"
    )
    db.add(base_map)
    db.commit()
    db.refresh(base_map)
    return base_map

@pytest.fixture
def test_vendor(db, test_project):
    from app.vendor.models import Vendor
    
    vendor = Vendor(
        project_id=test_project.project_id,
        vendor_name="Test Vendor",
        contact_person="Contact Person",
        phone="123-456-7890",
        responsibilities="Test responsibilities"
    )
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor

@pytest.fixture
def test_defect_category(db, test_project):
    from app.defect_category.models import DefectCategory
    
    category = DefectCategory(
        project_id=test_project.project_id,
        category_name="Test Category",
        description="Test description"
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@pytest.fixture
def test_defect(db, test_project, test_user, test_defect_category, test_vendor):
    from app.defect.models import Defect
    
    defect = Defect(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="Test defect description",
        assigned_vendor_id=test_vendor.vendor_id,
        expected_completion_day=datetime.now() + timedelta(days=7),
        status="等待中",
        created_at=datetime.utcnow()
    )
    db.add(defect)
    db.commit()
    db.refresh(defect)
    return defect

@pytest.fixture
def test_defect_mark(db, test_defect, test_base_map):
    from app.defect_mark.models import DefectMark
    
    defect_mark = DefectMark(
        defect_id=test_defect.defect_id,
        base_map_id=test_base_map.base_map_id,
        coordinate_x=100.0,
        coordinate_y=200.0,
        scale=1.0
    )
    db.add(defect_mark)
    db.commit()
    db.refresh(defect_mark)
    return defect_mark

@pytest.fixture
def test_photo(db, test_defect):
    from app.photo.models import Photo
    
    photo = Photo(
        related_type="defect",
        related_id=test_defect.defect_id,
        description="Test photo description",
        image_url="/path/to/image.jpg",
        created_at=datetime.utcnow()
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

@pytest.fixture
def test_improvement(db, test_defect, test_user):
    from app.improvement.models import Improvement
    
    improvement = Improvement(
        defect_id=test_defect.defect_id,
        submitter_id=test_user.user_id,
        content="Test improvement content",
        improvement_date="2023-01-01",
        created_at=datetime.utcnow()
    )
    db.add(improvement)
    db.commit()
    db.refresh(improvement)
    return improvement

@pytest.fixture
def test_confirmation(db, test_improvement, test_user):
    from app.confirmation.models import Confirmation
    
    confirmation = Confirmation(
        improvement_id=test_improvement.improvement_id,
        confirmer_id=test_user.user_id,
        status="接受",
        comment="Test confirmation comment",
        confirmation_date="2023-01-15",
        created_at=datetime.utcnow()
    )
    db.add(confirmation)
    db.commit()
    db.refresh(confirmation)
    return confirmation
