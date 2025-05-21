import pytest
from fastapi import status
from app.user.schemas import UserCreate, UserUpdate

# 欄位驗證測試 - 第一部分

def test_create_user_missing_required_field(client):
    """測試建立使用者時缺少必填欄位"""
    # 缺少 name 欄位（必填）
    user_data = {
        "line_id": "missing_name_line_id",
        "email": "missing_name@example.com",
        "company_name": "Missing Name Company"
    }
    
    # 發送請求
    response = client.post("/users/", json=user_data)
    
    # 檢查回應
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    # 確認錯誤訊息中包含 name 欄位
    assert any("name" in str(error["loc"]) for error in data["detail"])

def test_create_user_invalid_email_format(client):
    """測試建立使用者時 email 格式錯誤"""
    user_data = {
        "name": "Invalid Email User",
        "line_id": "invalid_email_line_id",
        "email": "not-an-email",  # 無效的 email 格式
        "company_name": "Invalid Email Company"
    }
    
    # 發送請求
    response = client.post("/users/", json=user_data)
    
    # 檢查回應
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    # 確認錯誤訊息中包含 email 欄位
    assert any("email" in str(error["loc"]) for error in data["detail"])

# 邊界情況測試 - 第一部分

def test_get_user_with_non_existent_id(client):
    """測試獲取不存在的使用者"""
    # 使用一個不太可能存在的 ID
    non_existent_id = 99999
    
    # 發送請求
    response = client.get(f"/users/{non_existent_id}")
    
    # 檢查回應
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"

def test_get_user_with_invalid_id_type(client):
    """測試使用無效的 ID 型別"""
    # 發送請求，使用字串而非整數
    response = client.get("/users/abc")
    
    # 檢查回應
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    # 只檢查狀態碼，不檢查具體錯誤訊息格式，因為這可能因實現而異
