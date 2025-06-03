import pytest
from fastapi import status
from app.confirmation import crud, schemas

# CRUD 測試

def test_create_confirmation(db, test_improvement, test_user):
    """測試建立確認單"""
    confirmation_data = schemas.ConfirmationCreate(
        improvement_id=test_improvement.improvement_id,
        confirmer_id=test_user.user_id,
        status="接受",
        comment="Test confirmation comment",
        confirmation_date="2023-01-15"
    )
    
    confirmation = crud.create_confirmation(db=db, confirmation=confirmation_data)
    assert confirmation.improvement_id == test_improvement.improvement_id
    assert confirmation.confirmer_id == test_user.user_id
    assert confirmation.status == "接受"
    assert confirmation.comment == "Test confirmation comment"
    assert confirmation.confirmation_date == "2023-01-15"
    assert confirmation.confirmation_id is not None

def test_get_confirmation(db, test_confirmation):
    """測試獲取單一確認單"""
    confirmation = crud.get_confirmation(db=db, confirmation_id=test_confirmation.confirmation_id)
    assert confirmation is not None
    assert confirmation.confirmation_id == test_confirmation.confirmation_id
    assert confirmation.improvement_id == test_confirmation.improvement_id
    assert confirmation.confirmer_id == test_confirmation.confirmer_id
    assert confirmation.status == test_confirmation.status
    assert confirmation.comment == test_confirmation.comment
    assert confirmation.confirmation_date == test_confirmation.confirmation_date

def test_get_confirmations(db, test_confirmation):
    """測試獲取所有確認單"""
    confirmations = crud.get_confirmations(db=db)
    assert len(confirmations) >= 1
    assert any(c.confirmation_id == test_confirmation.confirmation_id for c in confirmations)

def test_get_confirmations_by_improvement(db, test_confirmation, test_improvement):
    """測試依改善單獲取確認單"""
    confirmations = crud.get_confirmations_by_improvement(db=db, improvement_id=test_improvement.improvement_id)
    assert len(confirmations) >= 1
    assert any(c.confirmation_id == test_confirmation.confirmation_id for c in confirmations)

def test_get_confirmations_by_confirmer(db, test_confirmation, test_user):
    """測試依確認者獲取確認單"""
    confirmations = crud.get_confirmations_by_confirmer(db=db, confirmer_id=test_user.user_id)
    assert len(confirmations) >= 1
    assert any(c.confirmation_id == test_confirmation.confirmation_id for c in confirmations)

def test_get_confirmation_with_details(db, test_confirmation):
    """測試獲取確認單詳細資訊"""
    confirmation = crud.get_confirmation_with_details(db=db, confirmation_id=test_confirmation.confirmation_id)
    assert confirmation is not None
    assert confirmation["confirmation_id"] == test_confirmation.confirmation_id
    assert confirmation["improvement_id"] == test_confirmation.improvement_id
    assert confirmation["confirmer_id"] == test_confirmation.confirmer_id
    assert confirmation["status"] == test_confirmation.status
    assert confirmation["comment"] == test_confirmation.comment
    assert confirmation["confirmation_date"] == test_confirmation.confirmation_date
    assert "confirmer_name" in confirmation

def test_update_confirmation(db, test_confirmation):
    """測試更新確認單"""
    update_data = schemas.ConfirmationUpdate(
        status="拒絕",
        comment="Updated confirmation comment",
        confirmation_date="2023-02-15"
    )
    
    updated_confirmation = crud.update_confirmation(db=db, confirmation_id=test_confirmation.confirmation_id, confirmation=update_data)
    assert updated_confirmation is not None
    assert updated_confirmation.confirmation_id == test_confirmation.confirmation_id
    assert updated_confirmation.status == "拒絕"
    assert updated_confirmation.comment == "Updated confirmation comment"
    assert updated_confirmation.confirmation_date == "2023-02-15"

def test_delete_confirmation(db, test_confirmation):
    """測試刪除確認單"""
    result = crud.delete_confirmation(db=db, confirmation_id=test_confirmation.confirmation_id)
    assert result is True
    
    # 確認確認單已被刪除
    deleted_confirmation = crud.get_confirmation(db=db, confirmation_id=test_confirmation.confirmation_id)
    assert deleted_confirmation is None

# API 測試

def test_api_create_confirmation(client, test_improvement, test_user):
    """測試 API 建立確認單"""
    confirmation_data = {
        "improvement_id": test_improvement.improvement_id,
        "confirmer_id": test_user.user_id,
        "status": "接受",
        "comment": "API test confirmation",
        "confirmation_date": "2023-01-15"
    }
    
    response = client.post("/confirmations/", json=confirmation_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["improvement_id"] == test_improvement.improvement_id
    assert data["confirmer_id"] == test_user.user_id
    assert data["status"] == "接受"
    assert data["comment"] == "API test confirmation"
    assert data["confirmation_date"] == "2023-01-15"
    assert "confirmation_id" in data
    assert "created_at" in data

def test_api_read_confirmations(client, test_confirmation):
    """測試 API 獲取所有確認單"""
    response = client.get("/confirmations/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(c["confirmation_id"] == test_confirmation.confirmation_id for c in data)

def test_api_read_confirmations_by_improvement(client, test_confirmation, test_improvement):
    """測試 API 依改善單獲取確認單"""
    response = client.get(f"/confirmations/?improvement_id={test_improvement.improvement_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(c["confirmation_id"] == test_confirmation.confirmation_id for c in data)

def test_api_read_confirmations_by_confirmer(client, test_confirmation, test_user):
    """測試 API 依確認者獲取確認單"""
    response = client.get(f"/confirmations/?confirmer_id={test_user.user_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(c["confirmation_id"] == test_confirmation.confirmation_id for c in data)

def test_api_read_confirmation(client, test_confirmation):
    """測試 API 獲取單一確認單"""
    response = client.get(f"/confirmations/{test_confirmation.confirmation_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["confirmation_id"] == test_confirmation.confirmation_id
    assert data["improvement_id"] == test_confirmation.improvement_id
    assert data["confirmer_id"] == test_confirmation.confirmer_id
    assert data["status"] == test_confirmation.status
    assert data["comment"] == test_confirmation.comment
    assert data["confirmation_date"] == test_confirmation.confirmation_date

def test_api_read_confirmation_details(client, test_confirmation):
    """測試 API 獲取確認單詳細資訊"""
    response = client.get(f"/confirmations/{test_confirmation.confirmation_id}/details")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["confirmation_id"] == test_confirmation.confirmation_id
    assert data["improvement_id"] == test_confirmation.improvement_id
    assert data["confirmer_id"] == test_confirmation.confirmer_id
    assert data["status"] == test_confirmation.status
    assert data["comment"] == test_confirmation.comment
    assert data["confirmation_date"] == test_confirmation.confirmation_date
    assert "confirmer" in data
    assert "improvement" in data
    assert "defect" in data

def test_api_read_confirmation_not_found(client):
    """測試 API 獲取不存在的確認單"""
    response = client.get("/confirmations/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_update_confirmation(client, test_confirmation, test_user):
    """測試 API 更新確認單"""
    update_data = {
        "status": "拒絕",
        "comment": "API updated confirmation comment",
        "confirmation_date": "2023-02-15"
    }
    
    # 設置當前用戶為確認單確認者
    client.headers["X-Current-User-ID"] = str(test_confirmation.confirmer_id)
    
    response = client.put(f"/confirmations/{test_confirmation.confirmation_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["confirmation_id"] == test_confirmation.confirmation_id
    assert data["status"] == "拒絕"
    assert data["comment"] == "API updated confirmation comment"
    assert data["confirmation_date"] == "2023-02-15"

def test_api_update_confirmation_unauthorized(client, test_confirmation, test_user):
    """測試 API 未授權更新確認單"""
    update_data = {
        "status": "拒絕",
        "comment": "API updated confirmation comment",
        "confirmation_date": "2023-02-15"
    }
    
    # 設置當前用戶為非確認單確認者
    client.headers["X-Current-User-ID"] = "999"  # 假設這是另一個用戶ID
    
    response = client.put(f"/confirmations/{test_confirmation.confirmation_id}", json=update_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_api_update_confirmation_not_found(client, test_user):
    """測試 API 更新不存在的確認單"""
    update_data = {
        "status": "拒絕",
        "comment": "Updated confirmation comment",
        "confirmation_date": "2023-02-15"
    }
    
    # 設置當前用戶
    client.headers["X-Current-User-ID"] = str(test_user.user_id)
    
    response = client.put("/confirmations/9999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_confirmation(client, test_confirmation):
    """測試 API 刪除確認單"""
    # 設置當前用戶為確認單確認者
    client.headers["X-Current-User-ID"] = str(test_confirmation.confirmer_id)
    
    response = client.delete(f"/confirmations/{test_confirmation.confirmation_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_api_delete_confirmation_unauthorized(client, test_confirmation):
    """測試 API 未授權刪除確認單"""
    # 設置當前用戶為非確認單確認者
    client.headers["X-Current-User-ID"] = "999"  # 假設這是另一個用戶ID
    
    response = client.delete(f"/confirmations/{test_confirmation.confirmation_id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_api_delete_confirmation_not_found(client, test_user):
    """測試 API 刪除不存在的確認單"""
    # 設置當前用戶
    client.headers["X-Current-User-ID"] = str(test_user.user_id)
    
    response = client.delete("/confirmations/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
