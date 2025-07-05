import pytest
from fastapi import status
from datetime import datetime, date, timedelta
from app.defect import crud
from app.defect.schemas import DefectCreate, DefectUpdate

# CRUD Tests
def test_create_defect(db, test_project, test_user, test_defect_category, test_vendor):
    # Create test data
    defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-101",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="Test defect description",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        expected_completion_day=date.today() + timedelta(days=7),
        status="等待中"
    )
    
    # Create defect
    defect = crud.create_defect(db, defect_data)
    
    # Check defect was created correctly
    assert defect.project_id == test_project.project_id
    assert defect.submitted_id == test_user.user_id
    assert defect.defect_category_id == test_defect_category.defect_category_id
    assert defect.defect_description == "Test defect description"
    assert defect.assigned_vendor_id == test_vendor.vendor_id
    assert defect.responsible_vendor_id == test_vendor.vendor_id
    assert defect.status == "等待中"
    assert defect.defect_id is not None
    assert defect.created_at is not None
    assert defect.unique_code is not None
    assert isinstance(defect.unique_code, str)

def test_get_defect(db, test_defect):
    # Get defect
    defect = crud.get_defect(db, test_defect.defect_id)
    
    # Check defect was retrieved correctly
    assert defect is not None
    assert defect.defect_id == test_defect.defect_id
    assert defect.project_id == test_defect.project_id
    assert defect.submitted_id == test_defect.submitted_id
    assert defect.defect_category_id == test_defect.defect_category_id
    assert defect.defect_description == test_defect.defect_description
    assert defect.assigned_vendor_id == test_defect.assigned_vendor_id
    assert defect.responsible_vendor_id == test_defect.responsible_vendor_id
    assert defect.status == test_defect.status
    assert defect.unique_code == test_defect.unique_code
    assert isinstance(defect.unique_code, str)

def test_get_defects(db, test_defect):
    # Create another defect
    defect_data = DefectCreate(
        project_id=test_defect.project_id,
        submitted_id=test_defect.submitted_id,
        location="A标1F-102",
        defect_description="Another test defect description",
        status="改善中"
    )
    crud.create_defect(db, defect_data)
    
    # Get defects
    defects = crud.get_defects(db)
    
    # Check defects were retrieved correctly
    assert len(defects) >= 2
    assert any(d.defect_description == test_defect.defect_description for d in defects)
    assert any(d.defect_description == "Another test defect description" for d in defects)

def test_get_defects_with_filters(db, test_defect, test_project, test_user):
    # Test filtering by project
    defects = crud.get_defects(db, project_id=test_project.project_id)
    assert len(defects) >= 1
    assert all(d.project_id == test_project.project_id for d in defects)
    
    # Test filtering by submitter
    defects = crud.get_defects(db, submitted_id=test_user.user_id)
    assert len(defects) >= 1
    assert all(d.submitted_id == test_user.user_id for d in defects)
    
    # Test filtering by category
    if test_defect.defect_category_id:
        defects = crud.get_defects(db, defect_category_id=test_defect.defect_category_id)
        assert len(defects) >= 1
        assert all(d.defect_category_id == test_defect.defect_category_id for d in defects)
    
    # Test filtering by vendor
    if test_defect.assigned_vendor_id:
        defects = crud.get_defects(db, assigned_vendor_id=test_defect.assigned_vendor_id)
        assert len(defects) >= 1
        assert all(d.assigned_vendor_id == test_defect.assigned_vendor_id for d in defects)
    
    # Test filtering by status
    defects = crud.get_defects(db, status=test_defect.status)
    assert len(defects) >= 1
    assert all(d.status == test_defect.status for d in defects)

def test_update_defect(db, test_defect):
    # Create update data
    repair_description = "Test repair description"
    expected_completion_day = date.today() + timedelta(days=10)
    status = "已完成"
    confirmer_id = 1
    
    update_data = DefectUpdate(
        repair_description=repair_description,
        expected_completion_day=expected_completion_day,
        status=status,
        confirmer_id=confirmer_id
    )
    
    # Update defect
    updated_defect = crud.update_defect(db, test_defect.defect_id, update_data)
    
    # Check defect was updated correctly
    assert updated_defect is not None
    assert updated_defect.defect_id == test_defect.defect_id
    assert updated_defect.repair_description == repair_description
    assert updated_defect.expected_completion_day == expected_completion_day
    assert updated_defect.status == status

def test_delete_defect(db, test_defect):
    # Delete defect
    result = crud.delete_defect(db, test_defect.defect_id)
    
    # Check defect was deleted correctly
    assert result is True
    
    # Check defect no longer exists
    defect = crud.get_defect(db, test_defect.defect_id)
    assert defect is None

def test_get_defect_details(db, test_defect, test_project, test_user, test_defect_category, test_vendor):
    # Get defect with details
    defect_data = crud.get_defect_details(db, test_defect.defect_id, with_marks=True, with_photos=True, with_improvements=True, with_full_related=True)
    
    # Check defect data was retrieved correctly
    assert defect_data is not None
    assert defect_data["defect_id"] == test_defect.defect_id
    assert defect_data["project_id"] == test_defect.project_id
    assert defect_data["project_name"] == test_project.project_name
    assert defect_data["submitted_id"] == test_defect.submitted_id
    assert defect_data["submitter_name"] == test_user.name
    
    if test_defect.defect_category_id:
        assert defect_data["defect_category_id"] == test_defect.defect_category_id
        assert defect_data["category_name"] == test_defect_category.category_name
    
    assert defect_data["defect_description"] == test_defect.defect_description
    
    if test_defect.assigned_vendor_id:
        assert defect_data["assigned_vendor_id"] == test_defect.assigned_vendor_id
        assert defect_data["assigned_vendor_name"] == test_vendor.vendor_name
    
    if test_defect.responsible_vendor_id:
        assert defect_data["responsible_vendor_id"] == test_defect.responsible_vendor_id
        assert defect_data["responsible_vendor_name"] == test_vendor.vendor_name
    
    assert defect_data["status"] == test_defect.status

def test_get_defect_with_marks_and_photos(db, test_defect, test_defect_mark, test_photo):
    """此測試已棄用，功能已合併到 test_get_defect_details"""
    # 使用新的 get_defect_details 函數，但僅測試標記和照片
    defect_data = crud.get_defect_details(db, test_defect.defect_id, with_marks=True, with_photos=True)
    
    # 基本檢查
    assert defect_data is not None
    assert defect_data["defect_id"] == test_defect.defect_id
    
    # 檢查標記資料
    assert "defect_marks" in defect_data
    assert len(defect_data["defect_marks"]) >= 1
    assert any(mark["defect_mark_id"] == test_defect_mark.defect_mark_id for mark in defect_data["defect_marks"])
    
    # 檢查照片資料
    assert "photos" in defect_data
    assert len(defect_data["photos"]) >= 1
    assert any(photo["photo_id"] == test_photo.photo_id for photo in defect_data["photos"])

def test_get_defect_stats(db, test_defect, test_project):
    # Get defect stats
    stats = crud.get_defect_stats(db)
    
    # Check stats were retrieved correctly
    assert stats is not None
    assert "total_count" in stats
    assert stats["total_count"] >= 1
    assert "waiting_count" in stats
    assert "improving_count" in stats
    assert "pending_confirmation_count" in stats
    assert "completed_count" in stats
    assert "rejected_count" in stats
    assert "category_stats" in stats
    
    # Test project-specific stats
    project_stats = crud.get_defect_stats(db, project_id=test_project.project_id)
    assert project_stats is not None
    assert project_stats["total_count"] >= 1

# API Tests
def test_api_create_defect(client, test_project, test_user, test_defect_category, test_vendor):
    # Create test data
    # 使用今天日期加上7天作為預期完成日期
    expected_date = (date.today() + timedelta(days=7)).isoformat()
    
    defect_data = {
        "project_id": test_project.project_id,
        "submitted_id": test_user.user_id,
        "location": "A标1F-201",
        "defect_category_id": test_defect_category.defect_category_id,
        "defect_description": "API Test defect description",
        "assigned_vendor_id": test_vendor.vendor_id,
        "expected_completion_day": expected_date,
        "status": "等待中"
    }
    
    # Send request
    response = client.post("/defects/", json=defect_data)
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["project_id"] == test_project.project_id
    assert data["submitted_id"] == test_user.user_id
    assert data["defect_category_id"] == test_defect_category.defect_category_id
    assert data["defect_description"] == "API Test defect description"
    assert data["assigned_vendor_id"] == test_vendor.vendor_id
    assert data["status"] == "等待中"
    assert "defect_id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_api_read_defects(client, test_defect):
    # Send request
    response = client.get("/defects/")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # 找到測試缺失單的資料
    test_defect_data = next((d for d in data if d["defect_id"] == test_defect.defect_id), None)
    assert test_defect_data is not None
    
    # 檢查新增的欄位
    assert "project_name" in test_defect_data
    assert "submitter_name" in test_defect_data
    
    # 檢查分類名稱和廠商名稱（如果有的話）
    if test_defect.defect_category_id:
        assert "category_name" in test_defect_data
    
    if test_defect.assigned_vendor_id:
        assert "assigned_vendor_name" in test_defect_data
    
    if test_defect.responsible_vendor_id:
        assert "responsible_vendor_name" in test_defect_data

def test_api_read_defects_with_filters(client, test_defect, test_project, test_user, test_defect_category, test_vendor):
    # Test filtering by project
    response = client.get(f"/defects/?project_id={test_project.project_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert all(d["project_id"] == test_project.project_id for d in data)
    # 檢查專案名稱
    assert all(d["project_name"] == test_project.project_name for d in data)
    
    # Test filtering by submitter
    response = client.get(f"/defects/?submitted_id={test_user.user_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert all(d["submitted_id"] == test_user.user_id for d in data)
    # 檢查提交者名稱
    assert all(d["submitter_name"] == test_user.name for d in data)
    
    # Test filtering by category
    if test_defect.defect_category_id:
        response = client.get(f"/defects/?defect_category_id={test_defect.defect_category_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert all(d["defect_category_id"] == test_defect.defect_category_id for d in data)
        # 檢查分類名稱
        assert all(d["category_name"] == test_defect_category.category_name for d in data)
    
    # Test filtering by vendor
    if test_defect.assigned_vendor_id:
        response = client.get(f"/defects/?assigned_vendor_id={test_defect.assigned_vendor_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert all(d["assigned_vendor_id"] == test_defect.assigned_vendor_id for d in data)
        # 檢查廠商名稱
        assert all(d["assigned_vendor_name"] == test_vendor.vendor_name for d in data)
    
    # Test filtering by status
    response = client.get(f"/defects/?status={test_defect.status}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert all(d["status"] == test_defect.status for d in data)

def test_api_read_defect_stats(client, test_project):
    # 先確保有至少一個缺陷存在
    # 創建一個新的缺陷
    defect_data = {
        "project_id": test_project.project_id,
        "submitted_id": test_project.project_id,  # 使用 project_id 作為 user_id (僅測試用)
        "defect_description": "Stats Test defect description",
        "status": "等待中"
    }
    client.post("/defects/", json=defect_data)
    
    # Send request
    response = client.get("/defects/stats")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_count" in data
    # 只檢查統計數據的結構，不檢查具體數值
    assert "waiting_count" in data
    assert "improving_count" in data
    assert "pending_confirmation_count" in data
    assert "completed_count" in data
    assert "rejected_count" in data
    assert "category_stats" in data
    
    # Test project-specific stats
    response = client.get(f"/defects/stats?project_id={test_project.project_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # 確保至少有總數統計
    assert "total_count" in data

def test_api_read_defect(client, test_defect):
    # Send request
    response = client.get(f"/defects/{test_defect.defect_id}")
    
    # Check response data
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["defect_id"] == test_defect.defect_id
    assert data["project_id"] == test_defect.project_id
    assert data["submitted_id"] == test_defect.submitted_id
    assert data["defect_description"] == test_defect.defect_description
    assert data["status"] == test_defect.status
    assert data["unique_code"] == test_defect.unique_code

def test_api_read_defect_full(client, test_defect, test_defect_mark, test_photo):
    # 使用帶參數的 API 端點取得完整資料，使用 params 參數正確傳遞布林值
    params = {
        "with_marks": "true",
        "with_photos": "true",
        "with_improvements": "true",
        "with_full_related": "true"
    }
    response = client.get(f"/defects/{test_defect.defect_id}", params=params)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["defect_id"] == test_defect.defect_id

    # 檢查標記資料
    assert "defect_marks" in data
    assert len(data["defect_marks"]) >= 1
    
    # 檢查照片資料
    assert "photos" in data
    assert len(data["photos"]) >= 1
    
    # 檢查關聯資料
    if "project" in data:
        assert data["project"]["project_id"] == test_defect.project_id

def test_api_read_defect_not_found(client):
    # Send request with non-existent ID
    response = client.get("/defects/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_update_defect(client, test_defect):
    # Create update data
    expected_date = (date.today() + timedelta(days=10)).isoformat()
    defect_data = {
        "repair_description": "API Test repair description",
        "expected_completion_day": expected_date,
        "status": "已完成"
        # "confirmer_id" 欄位已經被移除
    }
    
    # Send request
    response = client.put(f"/defects/{test_defect.defect_id}", json=defect_data)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["defect_id"] == test_defect.defect_id
    assert data["repair_description"] == "API Test repair description"
    assert data["status"] == "已完成"

def test_api_update_defect_not_found(client):
    # Create update data
    defect_data = {
        "repair_description": "API Test repair description"
    }
    
    # Send request with non-existent ID
    response = client.put("/defects/999", json=defect_data)
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_defect(client, test_defect):
    # Send request
    response = client.delete(f"/defects/{test_defect.defect_id}")
    
    # Check response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Check defect no longer exists
    response = client.get(f"/defects/{test_defect.defect_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_defect_not_found(client):
    # Send request with non-existent ID
    response = client.delete("/defects/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND


# 新增測試案例：狀態轉換測試
def test_defect_status_transition(db, test_defect):
    # 測試從「等待中」到「改善中」
    update_data = DefectUpdate(status="改善中")
    updated_defect = crud.update_defect(db, test_defect.defect_id, update_data)
    assert updated_defect.status == "改善中"
    
    # 測試從「改善中」到「待確認」
    update_data = DefectUpdate(status="待確認")
    updated_defect = crud.update_defect(db, test_defect.defect_id, update_data)
    assert updated_defect.status == "待確認"
    
    # 測試確認完成
    update_data = DefectUpdate(status="已完成", confirmer_id=1)
    updated_defect = crud.update_defect(db, test_defect.defect_id, update_data)
    assert updated_defect.status == "已完成"
    assert updated_defect.confirmer_id == 1


# 新增測試案例：缺失單與改善單關聯測試
def test_defect_improvement_relation(db, test_defect, test_user):
    # 建立關聯的改善單
    from app.improvement.schemas import ImprovementCreate
    from app.improvement.crud import create_improvement, get_improvements_by_defect
    
    improvement_data = ImprovementCreate(
        defect_id=test_defect.defect_id,
        submitter_id=test_user.user_id,
        content="測試改善說明",
        improvement_date=datetime.utcnow().date()
    )
    improvement = create_improvement(db, improvement_data)
    
    # 確認改善單正確關聯到缺失單
    improvements = get_improvements_by_defect(db, test_defect.defect_id)
    assert len(improvements) >= 1
    assert any(imp.improvement_id == improvement.improvement_id for imp in improvements)
    
    # 使用 get_defect_details 取得完整資訊（包含改善單）
    defect_with_details = crud.get_defect_details(db, test_defect.defect_id, with_improvements=True)
    assert "improvements" in defect_with_details
    assert len(defect_with_details["improvements"]) >= 1
    assert any(imp["improvement_id"] == improvement.improvement_id for imp in defect_with_details["improvements"])


# 新增測試案例：複合條件篩選測試
def test_defect_multi_filter(db, test_defect, test_project, test_vendor):
    # 使用多個條件篩選
    filters = {
        "project_id": test_project.project_id,
        "assigned_vendor_id": test_vendor.vendor_id,
        "status": test_defect.status
    }
    results = crud.get_defects(db, **filters)
    
    # 確認結果符合所有篩選條件
    assert len(results) >= 1
    for defect in results:
        assert defect.project_id == test_project.project_id
        assert defect.assigned_vendor_id == test_vendor.vendor_id
        assert defect.status == test_defect.status


# 新增測試案例：時間相關測試
def test_defect_expected_completion(db, test_defect):
    # 設定預期完成日期
    expected_date = date.today() + timedelta(days=5)
    update_data = DefectUpdate(expected_completion_day=expected_date)
    updated_defect = crud.update_defect(db, test_defect.defect_id, update_data)
    
    # 檢查是否正確設定
    assert updated_defect.expected_completion_day == expected_date


# 新增測試案例：API 使用者操作測試
def test_api_update_defect_with_user(client, test_defect, test_user):
    # 在請求中直接包含使用者ID
    update_data = {
        "status": "已完成",
        "confirmer_id": test_user.user_id,  # 直接在請求中指定操作者
        "repair_description": "修復完成"
    }
    
    # 發送更新請求
    response = client.put(f"/defects/{test_defect.defect_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    
    # 驗證更新結果
    data = response.json()
    assert data["status"] == "已完成"
    assert data["confirmer_id"] == test_user.user_id
    assert data["repair_description"] == "修復完成"


# 新增測試案例：缺失單統計分析測試
def test_defect_statistics_detailed(db, test_defect, test_project):
    # 獲取缺失單統計
    stats = crud.get_defect_stats(db, project_id=test_project.project_id)
    
    # 檢查統計結果
    assert "total_count" in stats
    assert "waiting_count" in stats
    assert "improving_count" in stats
    assert "pending_confirmation_count" in stats
    assert "completed_count" in stats
    assert "rejected_count" in stats
    assert "category_stats" in stats
    
    # 確認總數大於等於各狀態數量之和
    status_sum = (
        stats["waiting_count"] +
        stats["improving_count"] +
        stats["pending_confirmation_count"] +
        stats["completed_count"] +
        stats["rejected_count"]
    )
    assert stats["total_count"] >= status_sum


# 新增測試案例：自動設定狀態測試 - 無前置缺失編號
def test_defect_status_without_previous_defect(db, test_project, test_user, test_defect_category, test_vendor):
    # 建立缺失單資料，不設定前置缺失編號和狀態
    defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-201",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="測試自動狀態設定 - 無前置缺失",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        expected_completion_day=date.today() + timedelta(days=7)
        # 不設定 previous_defect_id
        # 不設定 status
    )
    
    # 建立缺失單
    defect = crud.create_defect(db, defect_data)
    
    # 檢查狀態是否自動設為「等待中」
    assert defect.status == "等待中"


# 新增測試案例：自動設定狀態測試 - 有前置缺失編號（非已完成或退件）
def test_defect_status_with_previous_defect(db, test_defect, test_project, test_user, test_defect_category, test_vendor):
    # 先確保前置缺失不是已完成或退件狀態
    if test_defect.status in ["已完成", "退件"]:
        # 更新測試缺失單的狀態為等待中
        test_defect.status = "等待中"
        db.commit()
        db.refresh(test_defect)
    
    # 建立缺失單資料，設定前置缺失編號但不設定狀態
    defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-202",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="測試自動狀態設定 - 有前置缺失（非已完成或退件）",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        expected_completion_day=date.today() + timedelta(days=7),
        previous_defect_id=test_defect.defect_id  # 設定前置缺失編號
        # 不設定 status
    )
    
    # 建立缺失單
    defect = crud.create_defect(db, defect_data)
    
    # 檢查狀態是否自動設為「等待中」，因為前置缺失不是已完成或退件
    assert defect.status == "等待中"


# 新增測試案例：API 自動設定狀態測試 - 無前置缺失編號
def test_api_defect_status_without_previous_defect(client, test_project, test_user, test_defect_category, test_vendor):
    # 準備缺失單資料，不設定前置缺失編號和狀態
    defect_data = {
        "project_id": test_project.project_id,
        "submitted_id": test_user.user_id,
        "location": "A标1F-301",
        "defect_category_id": test_defect_category.defect_category_id,
        "defect_description": "API測試自動狀態設定 - 無前置缺失",
        "assigned_vendor_id": test_vendor.vendor_id,
        "responsible_vendor_id": test_vendor.vendor_id,
        "expected_completion_day": (date.today() + timedelta(days=7)).isoformat()
        # 不設定 previous_defect_id
        # 不設定 status
    }
    
    # 發送建立請求
    response = client.post("/defects/", json=defect_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # 檢查回應中的狀態是否為「等待中」
    data = response.json()
    assert data["status"] == "等待中"
    
    # 再次從資料庫確認狀態
    created_defect_id = data["defect_id"]
    db_defect = client.get(f"/defects/{created_defect_id}").json()
    assert db_defect["status"] == "等待中"


# 新增測試案例：API 自動設定狀態測試 - 有已完成的前置缺失編號
def test_api_defect_status_with_previous_defect(client, test_defect, test_project, test_user, test_defect_category, test_vendor, db):
    # 先將前置缺失設為已完成狀態
    test_defect.status = "已完成"
    db.commit()
    db.refresh(test_defect)
    
    # 準備缺失單資料，設定前置缺失編號但不設定狀態
    defect_data = {
        "project_id": test_project.project_id,
        "submitted_id": test_user.user_id,
        "location": "A标1F-302",
        "defect_category_id": test_defect_category.defect_category_id,
        "defect_description": "API測試自動狀態設定 - 有已完成的前置缺失",
        "assigned_vendor_id": test_vendor.vendor_id,
        "responsible_vendor_id": test_vendor.vendor_id,
        "expected_completion_day": (date.today() + timedelta(days=7)).isoformat(),
        "previous_defect_id": test_defect.defect_id  # 設定前置缺失編號
        # 不設定 status
    }
    
    # 發送建立請求
    response = client.post("/defects/", json=defect_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # 檢查回應中的狀態是否為「改善中」，因為前置缺失已完成
    data = response.json()
    assert data["status"] == "改善中"
    
    # 再次從資料庫確認狀態
    created_defect_id = data["defect_id"]
    db_defect = client.get(f"/defects/{created_defect_id}").json()
    assert db_defect["status"] == "改善中"


# 新增測試案例：自動設定狀態測試 - 前置缺失為已完成或退件狀態
def test_defect_status_with_completed_previous_defect(db, test_project, test_user, test_defect_category, test_vendor):
    # 先建立一個已完成的缺失單
    completed_defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-401",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="已完成的前置缺失",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        status="已完成"  # 設定為已完成狀態
    )
    completed_defect = crud.create_defect(db, completed_defect_data)
    
    # 建立新缺失單，其前置缺失為已完成的缺失單
    new_defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-402",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="測試自動狀態設定 - 前置缺失已完成",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        previous_defect_id=completed_defect.defect_id  # 設定前置缺失編號
        # 不設定 status
    )
    
    # 建立缺失單
    new_defect = crud.create_defect(db, new_defect_data)
    
    # 檢查狀態是否自動設為「改善中」，因為前置缺失已完成
    assert new_defect.status == "改善中"
    
    # 再測試一次退件狀態
    rejected_defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-403",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="退件的前置缺失",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        status="退件"  # 設定為退件狀態
    )
    rejected_defect = crud.create_defect(db, rejected_defect_data)
    
    # 建立新缺失單，其前置缺失為退件的缺失單
    another_defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-404",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="測試自動狀態設定 - 前置缺失退件",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        previous_defect_id=rejected_defect.defect_id  # 設定前置缺失編號
        # 不設定 status
    )
    
    # 建立缺失單
    another_defect = crud.create_defect(db, another_defect_data)
    
    # 檢查狀態是否自動設為「改善中」，因為前置缺失為退件
    assert another_defect.status == "改善中"


# 新增測試案例：更新缺失狀態時連動更新相關缺失單
def test_update_defect_status_updates_linked_defects(db, test_project, test_user, test_defect_category, test_vendor):
    # 先建立一個等待中的缺失單
    first_defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-501",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="前置缺失單",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        status="等待中"  # 設定為等待中狀態
    )
    first_defect = crud.create_defect(db, first_defect_data)
    
    # 建立一個以上述缺失為前置缺失的缺失單，狀態為等待中
    linked_defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-502",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="連動缺失單",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        previous_defect_id=first_defect.defect_id,
        status="等待中"  # 明確設定為等待中狀態
    )
    linked_defect = crud.create_defect(db, linked_defect_data)
    
    # 確認連動缺失單的狀態為等待中
    assert linked_defect.status == "等待中"
    
    # 更新前置缺失單的狀態為已完成
    update_data = DefectUpdate(status="已完成")
    updated_first_defect = crud.update_defect(db, first_defect.defect_id, update_data)
    
    # 重新查詢連動缺失單，確認其狀態已更新為改善中
    db.refresh(linked_defect)
    assert linked_defect.status == "改善中"
    
    # 再測試一次退件狀態
    # 先建立一個新的缺失單
    second_defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-503",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="另一個前置缺失單",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        status="等待中"  # 設定為等待中狀態
    )
    second_defect = crud.create_defect(db, second_defect_data)
    
    # 建立一個以上述缺失為前置缺失的缺失單，狀態為等待中
    another_linked_defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-504",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="另一個連動缺失單",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        previous_defect_id=second_defect.defect_id,
        status="等待中"  # 明確設定為等待中狀態
    )
    another_linked_defect = crud.create_defect(db, another_linked_defect_data)
    
    # 確認連動缺失單的狀態為等待中
    assert another_linked_defect.status == "等待中"
    
    # 更新前置缺失單的狀態為退件
    update_data = DefectUpdate(status="退件")
    updated_second_defect = crud.update_defect(db, second_defect.defect_id, update_data)
    
    # 重新查詢連動缺失單，確認其狀態已更新為改善中
    db.refresh(another_linked_defect)
    assert another_linked_defect.status == "改善中"


# 新增測試案例：API 更新缺失狀態時連動更新相關缺失單
def test_api_update_defect_status_updates_linked_defects(client, db, test_project, test_user, test_defect_category, test_vendor):
    # 先建立一個等待中的缺失單
    first_defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-601",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="API測試前置缺失單",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        status="等待中"  # 設定為等待中狀態
    )
    first_defect = crud.create_defect(db, first_defect_data)
    
    # 建立一個以上述缺失為前置缺失的缺失單，狀態為等待中
    linked_defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        location="A标1F-602",
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="API測試連動缺失單",
        assigned_vendor_id=test_vendor.vendor_id,
        responsible_vendor_id=test_vendor.vendor_id,
        previous_defect_id=first_defect.defect_id,
        status="等待中"  # 明確設定為等待中狀態
    )
    linked_defect = crud.create_defect(db, linked_defect_data)
    
    # 確認連動缺失單的狀態為等待中
    assert linked_defect.status == "等待中"
    
    # 透過 API 更新前置缺失單的狀態為已完成
    update_data = {"status": "已完成"}
    response = client.put(f"/defects/{first_defect.defect_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    
    # 重新查詢連動缺失單，確認其狀態已更新為改善中
    db.refresh(linked_defect)
    assert linked_defect.status == "改善中"
    
    # 再次確認透過 API 查詢的結果
    response = client.get(f"/defects/{linked_defect.defect_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "改善中"
