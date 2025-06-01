import pytest
import os
import io
from fastapi import status
from app.user import crud
from app.user.schemas import UserCreate, UserUpdate

def test_create_user_with_avatar(db):
    """測試創建帶有頭像路徑的使用者"""
    user_data = UserCreate(
        name="Avatar User",
        line_id="avatar_line_id",
        email="avatar@example.com",
        company_name="Avatar Company",
        avatar_path="static/avatar/custom.png"
    )
    
    user = crud.create_user(db, user_data)
    
    assert user.name == "Avatar User"
    assert user.avatar_path == "static/avatar/custom.png"
    assert user.user_id is not None

def test_update_user_avatar(db, test_user):
    """測試更新使用者頭像路徑"""
    update_data = UserUpdate(avatar_path="static/avatar/updated.png")
    
    updated_user = crud.update_user(db, test_user.user_id, update_data)
    
    assert updated_user.avatar_path == "static/avatar/updated.png"

def test_api_create_user_with_avatar(client):
    """測試通過 API 創建帶有頭像路徑的使用者"""
    user_data = {
        "name": "API Avatar User",
        "line_id": "api_avatar_line_id",
        "email": "api_avatar@example.com",
        "company_name": "API Avatar Company",
        "avatar_path": "static/avatar/api_custom.png"
    }
    
    response = client.post("/users/", json=user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["avatar_path"] == "static/avatar/api_custom.png"

def test_api_update_user_avatar(client, test_user):
    """測試通過 API 更新使用者頭像路徑"""
    update_data = {
        "avatar_path": "static/avatar/api_updated.png"
    }
    
    response = client.put(f"/users/{test_user.user_id}", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["avatar_path"] == "static/avatar/api_updated.png"

def test_api_upload_avatar(client, test_user, tmp_path):
    """測試通過 API 上傳使用者頭像"""
    # 創建一個測試文件
    test_file_path = tmp_path / "test_avatar.png"
    with open(test_file_path, "wb") as f:
        f.write(b"test file content")
    
    # 使用 TestClient 上傳文件
    with open(test_file_path, "rb") as f:
        response = client.post(
            f"/users/{test_user.user_id}/avatar",
            files={"file": ("test_avatar.png", f, "image/png")}
        )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["avatar_path"] == f"static/avatar/user_{test_user.user_id}.png"
    
    # 清理測試文件
    if os.path.exists(f"static/avatar/user_{test_user.user_id}.png"):
        os.remove(f"static/avatar/user_{test_user.user_id}.png")
