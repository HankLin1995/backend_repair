import pytest
import os
import io
from fastapi import status
from PIL import Image
from app.photo import crud, schemas

# CRUD 測試

def test_create_photo(db, test_defect):
    """測試建立照片"""
    photo_data = schemas.PhotoCreate(
        related_type="缺失單",
        related_id=test_defect.defect_id,
        description="Test photo description",
        image_url="/static/photos/test.jpg"
    )
    
    photo = crud.create_photo(db=db, photo=photo_data)
    assert photo.related_type == "缺失單"
    assert photo.related_id == test_defect.defect_id
    assert photo.description == "Test photo description"
    assert photo.image_url == "/static/photos/test.jpg"

def test_get_photo(db, test_photo):
    """測試獲取單一照片"""
    photo = crud.get_photo(db=db, photo_id=test_photo.photo_id)
    assert photo is not None
    assert photo.photo_id == test_photo.photo_id
    assert photo.related_type == test_photo.related_type
    assert photo.related_id == test_photo.related_id
    assert photo.description == test_photo.description
    assert photo.image_url == test_photo.image_url

def test_get_photos(db, test_photo):
    """測試獲取所有照片"""
    photos = crud.get_photos(db=db)
    assert len(photos) >= 1
    assert any(p.photo_id == test_photo.photo_id for p in photos)

def test_get_photos_by_related(db, test_photo, test_defect):
    """測試依關聯項目獲取照片"""
    photos = crud.get_photos_by_related(db=db, related_type="缺失單", related_id=test_defect.defect_id)
    assert len(photos) >= 1
    assert any(p.photo_id == test_photo.photo_id for p in photos)

def test_update_photo(db, test_photo):
    """測試更新照片"""
    update_data = schemas.PhotoUpdate(
        description="Updated description",
        image_url="/static/photos/updated.jpg"
    )
    
    updated_photo = crud.update_photo(db=db, photo_id=test_photo.photo_id, photo=update_data)
    assert updated_photo is not None
    assert updated_photo.photo_id == test_photo.photo_id
    assert updated_photo.description == "Updated description"
    assert updated_photo.image_url == "/static/photos/updated.jpg"

def test_delete_photo(db, test_photo):
    """測試刪除照片"""
    result = crud.delete_photo(db=db, photo_id=test_photo.photo_id)
    assert result is True
    
    # 確認照片已被刪除
    deleted_photo = crud.get_photo(db=db, photo_id=test_photo.photo_id)
    assert deleted_photo is None

# API 測試

def test_api_create_photo(client, test_defect):
    """測試 API 建立照片"""
    photo_data = {
        "related_type": "缺失單",
        "related_id": test_defect.defect_id,
        "description": "API test photo",
        "image_url": "/static/photos/api_test.jpg"
    }
    
    response = client.post("/photos/", json=photo_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["related_type"] == "缺失單"
    assert data["related_id"] == test_defect.defect_id
    assert data["description"] == "API test photo"
    assert data["image_url"] == "/static/photos/api_test.jpg"
    assert "photo_id" in data
    assert "created_at" in data
    assert "full_url" in data

def test_api_read_photos(client, test_photo):
    """測試 API 獲取所有照片"""
    response = client.get("/photos/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(p["photo_id"] == test_photo.photo_id for p in data)
    
    # 確認每個照片都有 full_url
    for photo in data:
        assert "full_url" in photo
        assert photo["full_url"].startswith("http")

def test_api_read_photos_by_related(client, test_photo, test_defect):
    """測試 API 依關聯項目獲取照片"""
    response = client.get(f"/photos/?related_type=缺失單&related_id={test_defect.defect_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(p["photo_id"] == test_photo.photo_id for p in data)

def test_api_read_photo(client, test_photo):
    """測試 API 獲取單一照片"""
    response = client.get(f"/photos/{test_photo.photo_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["photo_id"] == test_photo.photo_id
    assert data["related_type"] == test_photo.related_type
    assert data["related_id"] == test_photo.related_id
    assert data["description"] == test_photo.description
    assert data["image_url"] == test_photo.image_url
    assert "full_url" in data
    assert data["full_url"].startswith("http")

def test_api_read_photo_not_found(client):
    """測試 API 獲取不存在的照片"""
    response = client.get("/photos/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_update_photo(client, test_photo):
    """測試 API 更新照片"""
    update_data = {
        "description": "API updated description",
        "image_url": "/static/photos/api_updated.jpg"
    }
    
    response = client.put(f"/photos/{test_photo.photo_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["photo_id"] == test_photo.photo_id
    assert data["description"] == "API updated description"
    assert data["image_url"] == "/static/photos/api_updated.jpg"
    assert "full_url" in data
    assert data["full_url"].startswith("http")

def test_api_update_photo_not_found(client):
    """測試 API 更新不存在的照片"""
    update_data = {
        "description": "Updated description",
        "image_url": "/static/photos/updated.jpg"
    }
    
    response = client.put("/photos/9999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_photo(client, test_photo):
    """測試 API 刪除照片"""
    response = client.delete(f"/photos/{test_photo.photo_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_api_delete_photo_not_found(client):
    """測試 API 刪除不存在的照片"""
    response = client.delete("/photos/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

# 檔案上傳測試

def create_test_image():
    """創建測試用圖片"""
    file = io.BytesIO()
    image = Image.new('RGB', size=(100, 100), color=(255, 0, 0))
    image.save(file, 'jpeg')
    file.name = 'test.jpg'
    file.seek(0)
    return file

def test_api_upload_photo(client, test_defect):
    """測試 API 上傳照片檔案"""
    # 創建測試圖片
    test_image = create_test_image()
    
    # 準備表單資料
    files = {"file": ("test.jpg", test_image, "image/jpeg")}
    data = {
        "related_type": "缺失單",
        "related_id": str(test_defect.defect_id),
        "description": "Uploaded test photo"
    }
    
    # 發送請求
    response = client.post("/photos/upload/", files=files, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # 驗證回應
    data = response.json()
    assert data["related_type"] == "缺失單"
    assert data["related_id"] == test_defect.defect_id
    assert data["description"] == "Uploaded test photo"
    assert "image_url" in data
    assert data["image_url"].startswith("/static/photos/")
    assert "photo_id" in data
    assert "created_at" in data
    assert "full_url" in data
    assert data["full_url"].startswith("http")
    
    # 驗證檔案是否存在
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "static",
        "photos",
        os.path.basename(data["image_url"])
    )
    assert os.path.exists(file_path)
    
    # 清理測試檔案
    if os.path.exists(file_path):
        os.remove(file_path)
