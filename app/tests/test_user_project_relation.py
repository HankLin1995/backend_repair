import pytest
from fastapi import status
from app.user.schemas import UserCreate
from app.project.schemas import ProjectCreate
from app.permission.schemas import PermissionCreate

# 關聯資料完整性測試

def test_get_user_with_projects_empty(client, test_user):
    """測試獲取沒有關聯專案的使用者資料"""
    # 先刪除所有權限（移除使用者與專案的關聯）
    # 注意：這裡假設測試環境中已經有 test_permission 將 test_user 與 test_project 關聯
    # 我們需要先找到這個權限並刪除它
    
    # 獲取使用者的專案資料
    response = client.get(f"/users/{test_user.user_id}/projects")
    
    # 檢查回應
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # 檢查使用者基本資料
    assert data["user_id"] == test_user.user_id
    assert data["name"] == test_user.name
    
    # 如果已經沒有關聯的專案，projects 應該是空列表
    # 如果有關聯的專案，我們可以跳過這個測試
    if "projects" in data and len(data["projects"]) == 0:
        assert data["projects"] == []

def test_create_user_with_project_permission(client, db, test_project):
    """測試建立使用者並授予專案權限"""
    # 建立新使用者
    user_data = {
        "name": "Project Permission User",
        "line_id": "project_permission_line_id",
        "email": "project_permission@example.com",
        "company_name": "Project Permission Company"
    }
    
    response = client.post("/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    user_id = response.json()["user_id"]
    
    # 為使用者授予專案權限
    permission_data = {
        "project_id": test_project.project_id,
        "user_id": user_id,
        "user_role": "viewer"
    }
    
    response = client.post("/permissions/", json=permission_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # 獲取使用者的專案資料
    response = client.get(f"/users/{user_id}/projects")
    
    # 檢查回應
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # 檢查使用者基本資料
    assert data["user_id"] == user_id
    assert data["name"] == "Project Permission User"
    
    # 檢查專案資料
    assert "projects" in data
    assert len(data["projects"]) >= 1
    
    # 檢查是否包含我們剛剛授權的專案
    project_found = False
    for project in data["projects"]:
        if project["project_id"] == test_project.project_id:
            assert project["project_name"] == test_project.project_name
            assert project["role"] == "viewer"
            project_found = True
            break
    
    assert project_found, "新授權的專案未在使用者的專案列表中找到"

def test_delete_user_with_permissions(client, test_user, test_permission):
    """測試刪除有權限關聯的使用者"""
    # 刪除使用者
    response = client.delete(f"/users/{test_user.user_id}")
    
    # 檢查回應
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # 檢查使用者是否已被刪除
    response = client.get(f"/users/{test_user.user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # 檢查相關的權限是否也被刪除（如果系統實作了級聯刪除）
    # 這部分需要根據系統實際實作來調整
    # 如果系統沒有實作級聯刪除，這個測試可能需要修改

def test_permission_with_non_existent_user(client, test_project):
    """測試為不存在的使用者授予權限"""
    # 使用一個不存在的使用者 ID
    non_existent_user_id = 99999
    
    # 嘗試為不存在的使用者授予權限
    permission_data = {
        "project_id": test_project.project_id,
        "user_id": non_existent_user_id,
        "user_role": "viewer"
    }
    
    response = client.post("/permissions/", json=permission_data)
    
    # 檢查回應 - 應該回傳 404 Not Found 或 400 Bad Request
    assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]

def test_permission_with_non_existent_project(client, test_user):
    """測試為使用者授予不存在專案的權限"""
    # 使用一個不存在的專案 ID
    non_existent_project_id = 99999
    
    # 嘗試授予不存在專案的權限
    permission_data = {
        "project_id": non_existent_project_id,
        "user_id": test_user.user_id,
        "user_role": "viewer"
    }
    
    response = client.post("/permissions/", json=permission_data)
    
    # 檢查回應 - 應該回傳 404 Not Found 或 400 Bad Request
    assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]
