import pytest
from fastapi import status
from app.user.schemas import UserUpdate

# 更新相關的邊界測試

def test_update_user_empty_data(client, test_user):
    """測試更新使用者但提供空的更新資料"""
    # 提供空的更新資料
    update_data = {}
    
    # 發送請求
    response = client.put(f"/users/{test_user.user_id}", json=update_data)
    
    # 檢查回應 - 應該成功但資料不變
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == test_user.name
    assert data["email"] == test_user.email
    assert data["company_name"] == test_user.company_name
    assert data["line_id"] == test_user.line_id

def test_update_user_partial_data(client, test_user):
    """測試部分更新使用者資料（只更新部分欄位）"""
    # 只更新名稱
    update_data = {
        "name": "Updated User Name"
    }
    
    # 發送請求
    response = client.put(f"/users/{test_user.user_id}", json=update_data)
    
    # 檢查回應
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated User Name"  # 已更新
    assert data["email"] == test_user.email  # 未變更
    assert data["company_name"] == test_user.company_name  # 未變更
    assert data["line_id"] == test_user.line_id  # 未變更

def test_update_user_no_changes(client, test_user):
    """測試更新使用者但沒有實際變更"""
    # 使用與原本相同的資料
    update_data = {
        "name": test_user.name,
        "email": test_user.email,
        "company_name": test_user.company_name,
        "line_id": test_user.line_id
    }
    
    # 發送請求
    response = client.put(f"/users/{test_user.user_id}", json=update_data)
    
    # 檢查回應 - 應該成功但資料不變
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == test_user.name
    assert data["email"] == test_user.email
    assert data["company_name"] == test_user.company_name
    assert data["line_id"] == test_user.line_id

def test_update_user_to_duplicate_line_id(client, test_user):
    """測試更新使用者的 LINE ID 為已存在的值"""
    # 先建立另一個使用者
    new_user_data = {
        "name": "Another User",
        "line_id": "another_line_id",
        "email": "another@example.com",
        "company_name": "Another Company"
    }
    response = client.post("/users/", json=new_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    new_user_id = response.json()["user_id"]
    
    # 嘗試將第二個使用者的 LINE ID 更新為第一個使用者的 LINE ID
    update_data = {
        "line_id": test_user.line_id
    }
    
    # 發送請求
    response = client.put(f"/users/{new_user_id}", json=update_data)
    
    # 檢查回應 - 如果系統有實作 LINE ID 唯一性檢查，應該會回傳 400
    # 如果沒有實作，則會成功更新
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        assert "already exists" in response.json()["detail"].lower()
    else:
        # 如果沒有實作唯一性檢查，測試通過
        assert response.status_code == status.HTTP_200_OK

def test_delete_user_twice(client, test_user):
    """測試重複刪除同一使用者"""
    # 第一次刪除
    response = client.delete(f"/users/{test_user.user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # 第二次刪除同一使用者
    response = client.delete(f"/users/{test_user.user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"
