import pytest
from fastapi import status
from app.improvement import crud, schemas

# CRUD 測試

def test_create_improvement(db, test_defect, test_user):
    """測試建立改善單"""
    improvement_data = schemas.ImprovementCreate(
        defect_id=test_defect.defect_id,
        submitter_id=test_user.user_id,
        content="Test improvement content",
        improvement_date="2023-01-01"
    )
    
    improvement = crud.create_improvement(db=db, improvement=improvement_data)
    assert improvement.defect_id == test_defect.defect_id
    assert improvement.submitter_id == test_user.user_id
    assert improvement.content == "Test improvement content"
    assert improvement.improvement_date == "2023-01-01"
    assert improvement.improvement_id is not None

def test_get_improvement(db, test_improvement):
    """測試獲取單一改善單"""
    improvement = crud.get_improvement(db=db, improvement_id=test_improvement.improvement_id)
    assert improvement is not None
    assert improvement.improvement_id == test_improvement.improvement_id
    assert improvement.defect_id == test_improvement.defect_id
    assert improvement.submitter_id == test_improvement.submitter_id
    assert improvement.content == test_improvement.content
    assert improvement.improvement_date == test_improvement.improvement_date

def test_get_improvements(db, test_improvement):
    """測試獲取所有改善單"""
    improvements = crud.get_improvements(db=db)
    assert len(improvements) >= 1
    assert any(i.improvement_id == test_improvement.improvement_id for i in improvements)

def test_get_improvements_by_defect(db, test_improvement, test_defect):
    """測試依缺失單獲取改善單"""
    improvements = crud.get_improvements_by_defect(db=db, defect_id=test_defect.defect_id)
    assert len(improvements) >= 1
    assert any(i.improvement_id == test_improvement.improvement_id for i in improvements)

def test_get_improvements_by_submitter(db, test_improvement, test_user):
    """測試依提交者獲取改善單"""
    improvements = crud.get_improvements_by_submitter(db=db, submitter_id=test_user.user_id)
    assert len(improvements) >= 1
    assert any(i.improvement_id == test_improvement.improvement_id for i in improvements)

def test_get_improvement_with_details(db, test_improvement):
    """測試獲取改善單詳細資訊"""
    improvement = crud.get_improvement_with_details(db=db, improvement_id=test_improvement.improvement_id)
    assert improvement is not None
    assert improvement["improvement_id"] == test_improvement.improvement_id
    assert improvement["defect_id"] == test_improvement.defect_id
    assert improvement["submitter_id"] == test_improvement.submitter_id
    assert improvement["content"] == test_improvement.content
    assert improvement["improvement_date"] == test_improvement.improvement_date
    assert "submitter_name" in improvement
    assert "defect_description" in improvement

def test_update_improvement(db, test_improvement):
    """測試更新改善單"""
    update_data = schemas.ImprovementUpdate(
        content="Updated improvement content",
        improvement_date="2023-02-01"
    )
    
    updated_improvement = crud.update_improvement(db=db, improvement_id=test_improvement.improvement_id, improvement=update_data)
    assert updated_improvement is not None
    assert updated_improvement.improvement_id == test_improvement.improvement_id
    assert updated_improvement.content == "Updated improvement content"
    assert updated_improvement.improvement_date == "2023-02-01"

def test_delete_improvement(db, test_improvement):
    """測試刪除改善單"""
    result = crud.delete_improvement(db=db, improvement_id=test_improvement.improvement_id)
    assert result is True
    
    # 確認改善單已被刪除
    deleted_improvement = crud.get_improvement(db=db, improvement_id=test_improvement.improvement_id)
    assert deleted_improvement is None

# API 測試

def test_api_create_improvement(client, test_defect, test_user):
    """測試 API 建立改善單"""
    improvement_data = {
        "defect_id": test_defect.defect_id,
        "submitter_id": test_user.user_id,
        "content": "API test improvement",
        "improvement_date": "2023-01-01"
    }
    
    response = client.post("/improvements/", json=improvement_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["defect_id"] == test_defect.defect_id
    assert data["submitter_id"] == test_user.user_id
    assert data["content"] == "API test improvement"
    assert data["improvement_date"] == "2023-01-01"
    assert "improvement_id" in data
    assert "created_at" in data

def test_api_read_improvements(client, test_improvement):
    """測試 API 獲取所有改善單"""
    response = client.get("/improvements/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(i["improvement_id"] == test_improvement.improvement_id for i in data)

def test_api_read_improvements_by_defect(client, test_improvement, test_defect):
    """測試 API 依缺失單獲取改善單"""
    response = client.get(f"/improvements/?defect_id={test_defect.defect_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(i["improvement_id"] == test_improvement.improvement_id for i in data)

def test_api_read_improvements_by_submitter(client, test_improvement, test_user):
    """測試 API 依提交者獲取改善單"""
    response = client.get(f"/improvements/?submitter_id={test_user.user_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(i["improvement_id"] == test_improvement.improvement_id for i in data)

def test_api_read_improvement(client, test_improvement):
    """測試 API 獲取單一改善單"""
    response = client.get(f"/improvements/{test_improvement.improvement_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["improvement_id"] == test_improvement.improvement_id
    assert data["defect_id"] == test_improvement.defect_id
    assert data["submitter_id"] == test_improvement.submitter_id
    assert data["content"] == test_improvement.content
    assert data["improvement_date"] == test_improvement.improvement_date

def test_api_read_improvement_details(client, test_improvement):
    """測試 API 獲取改善單詳細資訊"""
    response = client.get(f"/improvements/{test_improvement.improvement_id}/details")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["improvement_id"] == test_improvement.improvement_id
    assert data["defect_id"] == test_improvement.defect_id
    assert data["submitter_id"] == test_improvement.submitter_id
    assert data["content"] == test_improvement.content
    assert data["improvement_date"] == test_improvement.improvement_date
    assert "submitter_name" in data
    assert "defect_description" in data

def test_api_read_improvement_not_found(client):
    """測試 API 獲取不存在的改善單"""
    response = client.get("/improvements/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_update_improvement(client, test_improvement, test_user):
    """測試 API 更新改善單"""
    update_data = {
        "content": "API updated improvement content",
        "improvement_date": "2023-02-01"
    }
    
    # 設置當前用戶為改善單提交者
    client.headers["X-Current-User-ID"] = str(test_improvement.submitter_id)
    
    response = client.put(f"/improvements/{test_improvement.improvement_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["improvement_id"] == test_improvement.improvement_id
    assert data["content"] == "API updated improvement content"
    assert data["improvement_date"] == "2023-02-01"

def test_api_update_improvement_unauthorized(client, test_improvement, test_user):
    """測試 API 未授權更新改善單"""
    update_data = {
        "content": "API updated improvement content",
        "improvement_date": "2023-02-01"
    }
    
    # 設置當前用戶為非改善單提交者
    client.headers["X-Current-User-ID"] = "999"  # 假設這是另一個用戶ID
    
    response = client.put(f"/improvements/{test_improvement.improvement_id}", json=update_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_api_update_improvement_not_found(client, test_user):
    """測試 API 更新不存在的改善單"""
    update_data = {
        "content": "Updated improvement content",
        "improvement_date": "2023-02-01"
    }
    
    # 設置當前用戶
    client.headers["X-Current-User-ID"] = str(test_user.user_id)
    
    response = client.put("/improvements/9999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_improvement(client, test_improvement):
    """測試 API 刪除改善單"""
    # 設置當前用戶為改善單提交者
    client.headers["X-Current-User-ID"] = str(test_improvement.submitter_id)
    
    response = client.delete(f"/improvements/{test_improvement.improvement_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_api_delete_improvement_unauthorized(client, test_improvement):
    """測試 API 未授權刪除改善單"""
    # 設置當前用戶為非改善單提交者
    client.headers["X-Current-User-ID"] = "999"  # 假設這是另一個用戶ID
    
    response = client.delete(f"/improvements/{test_improvement.improvement_id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_api_delete_improvement_not_found(client, test_user):
    """測試 API 刪除不存在的改善單"""
    # 設置當前用戶
    client.headers["X-Current-User-ID"] = str(test_user.user_id)
    
    response = client.delete("/improvements/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
