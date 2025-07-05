# Product Requirements Document (PRD) - API Router Implementations

## 已實現的 API 路由功能 (Implemented API Router Functionalities)

本節列出了 `app/` 目錄下各模組中已實現的 API 路由端點及其功能描述。

### 1. `base_map/routers.py` (基礎地圖)

*   **POST /**
    *   **功能**: 建立一個新的基礎地圖。
*   **GET /**
    *   **功能**: 獲取基礎地圖列表，支援分頁和按專案 ID 過濾。
*   **GET /project/{project_id}/with-counts**
    *   **功能**: 獲取指定專案的基礎地圖列表，並包含每個地圖上的缺失標記數量。
*   **GET /{base_map_id}**
    *   **功能**: 獲取指定 ID 的基礎地圖。
*   **PUT /{base_map_id}**
    *   **功能**: 更新指定 ID 的基礎地圖。
*   **DELETE /{base_map_id}**
    *   **功能**: 刪除指定 ID 的基礎地圖。
*   **POST /{base_map_id}/image**
    *   **功能**: 上傳基礎地圖圖片。

### 2. `confirmation/routers.py` (確認單)

*   **POST /**
    *   **功能**: 建立一個新的確認記錄。
*   **GET /{confirmation_id}**
    *   **功能**: 獲取指定 ID 的確認單。
*   **GET /**
    *   **功能**: 獲取確認單列表，支援分頁和按改善單 ID、確認者 ID、狀態過濾。
*   **PUT /{confirmation_id}**
    *   **功能**: 更新指定 ID 的確認單。
*   **DELETE /{confirmation_id}**
    *   **功能**: 刪除指定 ID 的確認單。
*   **GET /{confirmation_id}/details**
    *   **功能**: 獲取指定 ID 確認單的詳細資訊。

### 3. `defect/routers.py` (缺失單)

*   **POST /**
    *   **功能**: 建立一個新的缺失單。
*   **GET /**
    *   **功能**: 獲取缺失單列表，支援分頁和按專案 ID、提交者 ID、缺失類別 ID、指派廠商 ID、狀態過濾。
*   **GET /stats**
    *   **功能**: 獲取缺失統計數據。
*   **GET /unique_code/{unique_code}**
    *   **功能**: 獲取指定唯一代碼的缺失單。
*   **GET /{defect_id}**
    *   **功能**: 獲取指定 ID 缺失單的詳細資訊，可選擇包含標記、照片、改善和完整關聯實體資料。
*   **GET /{defect_id}/full** (已棄用)
    *   **功能**: [已棄用] 獲取指定 ID 缺失單的完整詳細資訊。
*   **PUT /{defect_id}**
    *   **功能**: 更新指定 ID 的缺失單。
*   **DELETE /{defect_id}**
    *   **功能**: 刪除指定 ID 的缺失單。

### 4. `defect_category/routers.py` (缺失類別)

*   **POST /**
    *   **功能**: 建立一個新的缺失類別。
*   **GET /**
    *   **功能**: 獲取缺失類別列表，支援分頁。
*   **GET /with-counts**
    *   **功能**: 獲取缺失類別列表，並包含每個類別所屬的缺失數量。
*   **GET /{defect_category_id}**
    *   **功能**: 獲取指定 ID 的缺失類別。
*   **PUT /{defect_category_id}**
    *   **功能**: 更新指定 ID 的缺失類別。
*   **DELETE /{defect_category_id}**
    *   **功能**: 刪除指定 ID 的缺失類別。

### 5. `defect_mark/routers.py` (缺失標記)

*   **POST /**
    *   **功能**: 建立一個新的缺失標記。
*   **GET /**
    *   **功能**: 獲取缺失標記列表，支援分頁和按缺失 ID、基礎地圖 ID 過濾。
*   **GET /with-details**
    *   **功能**: 獲取缺失標記列表，並包含缺失和基礎地圖的詳細資訊。
*   **GET /{defect_mark_id}**
    *   **功能**: 獲取指定 ID 的缺失標記。
*   **PUT /{defect_mark_id}**
    *   **功能**: 更新指定 ID 的缺失標記。
*   **DELETE /{defect_mark_id}**
    *   **功能**: 刪除指定 ID 的缺失標記。

### 6. `improvement/routers.py` (改善單)

*   **POST /**
    *   **功能**: 建立一個新的改善記錄。
*   **GET /{improvement_id}**
    *   **功能**: 獲取指定 ID 的改善單。
*   **GET /**
    *   **功能**: 獲取改善單列表，支援分頁和按缺失 ID、提交者 ID 過濾。
*   **PUT /{improvement_id}**
    *   **功能**: 更新指定 ID 的改善單。
*   **DELETE /{improvement_id}**
    *   **功能**: 刪除指定 ID 的改善單。
*   **GET /{improvement_id}/details**
    *   **功能**: 獲取指定 ID 改善單的詳細資訊。

### 7. `permission/routers.py` (權限)

*   **POST /**
    *   **功能**: 建立一個新的權限記錄。
*   **GET /**
    *   **功能**: 獲取權限列表，支援分頁和按專案 ID、使用者電子郵件過濾。
*   **GET /{permission_id}**
    *   **功能**: 獲取指定 ID 的權限記錄。
*   **PUT /{permission_id}**
    *   **功能**: 更新指定 ID 的權限記錄。
*   **DELETE /{permission_id}**
    *   **功能**: 刪除指定 ID 的權限記錄。

### 8. `photo/routers.py` (照片)

*   **POST /**
    *   **功能**: 上傳新的照片檔案。
*   **GET /**
    *   **功能**: 獲取照片列表，支援分頁和按關聯類型、關聯 ID 過濾。
*   **GET /{photo_id}**
    *   **功能**: 獲取指定 ID 的照片。
*   **PUT /{photo_id}**
    *   **功能**: 更新指定 ID 的照片。
*   **DELETE /{photo_id}**
    *   **功能**: 刪除指定 ID 的照片。

### 9. `project/routers.py` (專案)

*   **POST /**
    *   **功能**: 建立一個新的專案。
*   **GET /**
    *   **功能**: 獲取專案列表，支援分頁。
*   **GET /{project_id}**
    *   **功能**: 獲取指定 ID 的專案。
*   **GET /{project_id}/with-counts**
    *   **功能**: 獲取指定 ID 專案的相關實體數量統計。
*   **POST /{project_id}/image**
    *   **功能**: 上傳專案圖片。
*   **GET /{project_id}/with-roles**
    *   **功能**: 獲取專案中存在的使用者角色。
*   **PUT /{project_id}**
    *   **功能**: 更新指定 ID 的專案。
*   **DELETE /{project_id}**
    *   **功能**: 刪除指定 ID 的專案（同時刪除相關的基礎地圖檔案）。

### 10. `user/routers.py` (使用者)

*   **POST /**
    *   **功能**: 建立一個新的使用者。
*   **GET /**
    *   **功能**: 獲取使用者列表，支援分頁。
*   **GET /{user_id}**
    *   **功能**: 獲取指定 ID 的使用者。
*   **GET /line/{line_id}**
    *   **功能**: 獲取指定 LINE ID 的使用者。
*   **GET /{user_id}/projects**
    *   **功能**: 獲取指定使用者及其所屬專案和角色。
*   **PUT /{user_id}**
    *   **功能**: 更新指定 ID 的使用者。
*   **DELETE /{user_id}**
    *   **功能**: 刪除指定 ID 的使用者。
*   **POST /{user_id}/avatar**
    *   **功能**: 上傳使用者頭像。

### 11. `vendor/routers.py` (廠商)

*   **POST /**
    *   **功能**: 建立一個新的廠商。
*   **GET /**
    *   **功能**: 獲取廠商列表，支援分頁。
*   **GET /with-counts**
    *   **功能**: 獲取廠商列表，並包含每個廠商所指派的缺失數量。
*   **GET /{vendor_id}**
    *   **功能**: 獲取指定 ID 的廠商。
*   **PUT /{vendor_id}**
    *   **功能**: 更新指定 ID 的廠商。
*   **DELETE /{vendor_id}**
    *   **功能**: 刪除指定 ID 的廠商。
