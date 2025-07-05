# Product Requirements Document (PRD) - Backend Defect Management System

## 模組分析 (Module Analysis)

以下是對 `@app` 目錄下各模組的分析，並以列表形式總結其功能：

### 模組詳情

1.  **`base_map/`**:
    *   **目的 (Purpose)**: 管理與特定專案相關的基礎地圖（例如，樓層平面圖、場地圖）。
    *   **功能 (Functionality)**: 提供基礎地圖的 CRUD（建立、讀取、更新、刪除）操作，允許上傳基礎地圖圖片檔案，並能檢索基礎地圖以及相關聯的缺失標記數量。

2.  **`confirmation/`**:
    *   **目的 (Purpose)**: 處理針對缺失改善的確認流程。
    *   **功能 (Functionality)**: 允許使用者建立、檢索、更新和刪除確認記錄。關鍵的是，它會根據確認狀態（"接受" 或 "退回"）更新相關缺失的狀態（例如，更新為 "已完成" 或 "改善中"）。它還提供詳細的確認資訊，包括相關改善和缺失的描述。

3.  **`defect/`**:
    *   **目的 (Purpose)**: 缺陷管理系統的核心模組。
    *   **功能 (Functionality)**: 提供缺失的全面 CRUD 操作，包括唯一代碼、位置、類別、指派/負責廠商以及狀態追蹤。它支援廣泛的篩選、檢索詳細缺失資訊（包括相關標記、照片和改善），並生成缺失統計數據（總數、按狀態、按類別）。

4.  **`defect_category/`**:
    *   **目的 (Purpose)**: 管理專案中用於分類缺失的類別。
    *   **功能 (Functionality)**: 提供缺失類別的 CRUD 操作，並能檢索類別以及每個類別所屬的缺失數量。

5.  **`defect_mark/`**:
    *   **目的 (Purpose)**: 管理基礎地圖上缺失標記的放置。
    *   **功能 (Functionality)**: 提供缺失標記的 CRUD 操作，儲存其座標和比例。它將標記連結到特定的缺失和基礎地圖，並允許檢索標記以及相關缺失和基礎地圖的詳細資訊。

6.  **`improvement/`**:
    *   **目的 (Purpose)**: 管理針對缺失所做的改善記錄。
    *   **功能 (Functionality)**: 提供改善記錄的 CRUD 操作，追蹤改善的內容、提交者和日期。它允許按缺失或提交者篩選檢索改善，並提供詳細的改善資訊。

7.  **`permission/`**:
    *   **目的 (Purpose)**: 管理專案中的使用者存取權限。
    *   **功能 (Functionality)**: 定義和管理特定專案的使用者角色（例如，管理員、編輯者、檢視者）。它支援建立、檢索、更新和刪除權限，並能提供詳細的權限資訊，包括專案和使用者詳細資訊。

8.  **`photo/`**:
    *   **目的 (Purpose)**: 處理與各種實體相關聯的照片上傳、儲存和檢索。
    *   **功能 (Functionality)**: 允許上傳圖片檔案，並將其與缺失、改善或確認單關聯。它管理檔案儲存，為存取照片生成唯一的 URL，並提供照片記錄的 CRUD 操作。

9.  **`project/`**:
    *   **目的 (Purpose)**: 管理專案層級的資訊。
    *   **功能 (Functionality)**: 提供專案的 CRUD 操作，包括專案名稱和相關圖片。它提供聚合數據，例如專案中的基礎地圖、缺失和使用者數量，並能檢索特定專案的使用者角色。它還包含一項服務，確保在刪除專案時，相關的基礎地圖圖片檔案也會被刪除。

10. **`user/`**:
    *   **目的 (Purpose)**: 管理使用者帳戶和個人資料。
    *   **功能 (Functionality)**: 提供使用者帳戶的 CRUD 操作，包括個人詳細資訊、LINE ID、電子郵件、公司和頭像。它支援按 LINE ID 檢索使用者，並能列出使用者的相關專案及其在這些專案中的角色。它還處理頭像上傳。

11. **`vendor/`**:
    *   **目的 (Purpose)**: 管理廠商（承包商）的資訊。
    *   **功能 (Functionality)**: 提供廠商記錄的 CRUD 操作，包括聯絡方式和職責。它能檢索廠商並顯示指派給每個廠商的缺失數量。

### 總結 (Conclusion)

`@app` 目錄包含一個模組化的後端系統，用於管理建築缺陷，其結構圍繞著關鍵實體及其關係：

*   **`project/`**: 組織工作的核心實體，管理專案詳細資訊並提供高層次統計數據。
*   **`user/`**: 管理使用者帳戶、個人資料及其專案隸屬關係/角色。
*   **`permission/`**: 控制特定專案中的使用者存取和角色。
*   **`vendor/`**: 管理承包商資訊並追蹤其指派的缺失。
*   **`defect_category/`**: 提供缺失分類系統。
*   **`base_map/`**: 管理可以標記缺失的樓層平面圖或場地圖。
*   **`defect/`**: 核心模組，用於詳細的缺失追蹤，包括狀態、指派和相關資訊。
*   **`defect_mark/`**: 將缺失連結到基礎地圖上的特定位置。
*   **`photo/`**: 處理圖片上傳並與各種記錄（缺失、改善、確認單）關聯。
*   **`improvement/`**: 追蹤為解決缺失而採取的行動。
*   **`confirmation/`**: 管理改善的批准/拒絕流程，影響缺失狀態。

這種結構表明了一個定義明確的缺陷管理系統 API，每個領域實體都有明確的職責劃分。

## 資料庫模型與關係 (Database Models and Relationships)

本節詳細說明系統中的主要資料庫表、其欄位定義以及表之間的相互連結。

### 核心資料表 (Core Tables)

#### 1. `projects` (專案)

*   **描述**: 儲存專案的基本資訊。
*   **欄位**:
    *   `project_id` (Integer, Primary Key): 專案唯一識別碼。
    *   `project_name` (String): 專案名稱。
    *   `created_at` (DateTime): 專案建立時間。
    *   `image_path` (String): 專案圖片路徑。
    *   `unique_code` (String, Unique): 專案的唯一代碼。
*   **關係**:
    *   一對多 (`permissions`): 一個專案可以有多個權限設定。
    *   一對多 (`base_maps`): 一個專案可以有多個基礎地圖。
    *   一對多 (`defects`): 一個專案可以有多個缺失。
    *   一對多 (`vendors`): 一個專案可以有多個廠商。
    *   一對多 (`defect_categories`): 一個專案可以有多個缺失類別。

#### 2. `users` (使用者)

*   **描述**: 儲存使用者帳戶資訊。
*   **欄位**:
    *   `user_id` (Integer, Primary Key): 使用者唯一識別碼。
    *   `line_id` (String): 使用者的 LINE ID。
    *   `name` (String): 使用者姓名。
    *   `email` (String): 使用者電子郵件。
    *   `company_name` (String): 使用者所屬公司名稱。
    *   `avatar_path` (String): 使用者頭像圖片路徑。
    *   `created_at` (DateTime): 使用者帳戶建立時間。
*   **關係**:
    *   一對多 (`submitted_defects`): 一個使用者可以提交多個缺失。
    *   一對多 (`submitted_improvements`): 一個使用者可以提交多個改善。
    *   一對多 (`confirmations`): 一個使用者可以進行多個確認。

#### 3. `permissions` (權限)

*   **描述**: 定義使用者在特定專案中的角色。
*   **欄位**:
    *   `permission_id` (Integer, Primary Key): 權限記錄唯一識別碼。
    *   `project_id` (Integer, Foreign Key to `projects`): 專案識別碼。
    *   `user_email` (String): 使用者電子郵件 (非外鍵，但邏輯關聯 `users.email`)。
    *   `user_role` (String): 使用者在專案中的角色 (e.g., "admin", "editor", "viewer")。
*   **關係**:
    *   多對一 (`project`): 多個權限記錄屬於一個專案。

#### 4. `vendors` (廠商)

*   **描述**: 儲存廠商資訊。
*   **欄位**:
    *   `vendor_id` (Integer, Primary Key): 廠商唯一識別碼。
    *   `project_id` (Integer, Foreign Key to `projects`): 廠商所屬專案識別碼。
    *   `vendor_name` (String): 廠商名稱。
    *   `contact_person` (String): 聯絡人姓名。
    *   `phone` (String): 聯絡電話。
    *   `responsibilities` (Text): 廠商職責描述。
    *   `email` (String): 廠商電子郵件。
    *   `line_id` (String): 廠商 LINE ID。
    *   `unique_code` (String, Unique): 廠商的唯一代碼。
*   **關係**:
    *   多對一 (`project`): 多個廠商屬於一個專案。
    *   一對多 (`assigned_defects`): 一個廠商可以被指派多個缺失。
    *   一對多 (`responsible_defects`): 一個廠商可以負責多個缺失。

#### 5. `defect_categories` (缺失類別)

*   **描述**: 儲存缺失的分類資訊。
*   **欄位**:
    *   `defect_category_id` (Integer, Primary Key): 缺失類別唯一識別碼。
    *   `project_id` (Integer, Foreign Key to `projects`): 缺失類別所屬專案識別碼。
    *   `category_name` (String): 類別名稱。
    *   `description` (Text): 類別描述。
*   **關係**:
    *   多對一 (`project`): 多個缺失類別屬於一個專案。
    *   一對多 (`defects`): 一個缺失類別可以包含多個缺失。

#### 6. `base_maps` (基礎地圖)

*   **描述**: 儲存專案的基礎地圖資訊。
*   **欄位**:
    *   `base_map_id` (Integer, Primary Key): 基礎地圖唯一識別碼。
    *   `project_id` (Integer, Foreign Key to `projects`): 基礎地圖所屬專案識別碼。
    *   `map_name` (String): 地圖名稱。
    *   `file_path` (String): 地圖圖片檔案路徑。
*   **關係**:
    *   多對一 (`project`): 多個基礎地圖屬於一個專案。
    *   一對多 (`defect_marks`): 一個基礎地圖可以有多個缺失標記。

#### 7. `defects` (缺失)

*   **描述**: 儲存詳細的缺失資訊。
*   **欄位**:
    *   `defect_id` (Integer, Primary Key): 缺失唯一識別碼。
    *   `unique_code` (String, Unique): 缺失的唯一代碼。
    *   `project_id` (Integer, Foreign Key to `projects`): 缺失所屬專案識別碼。
    *   `submitted_id` (Integer, Foreign Key to `users`): 缺失提交者識別碼。
    *   `location` (String): 缺失地點描述。
    *   `defect_category_id` (Integer, Foreign Key to `defect_categories`): 缺失類別識別碼。
    *   `defect_description` (Text): 缺失詳細描述。
    *   `assigned_vendor_id` (Integer, Foreign Key to `vendors`): 指派廠商識別碼。
    *   `repair_description` (Text): 修復描述。
    *   `expected_completion_day` (Date): 預計完成日期。
    *   `responsible_vendor_id` (Integer, Foreign Key to `vendors`): 責任廠商識別碼。
    *   `previous_defect_id` (Integer, Foreign Key to `defects`): 前置缺失單識別碼 (用於追蹤重複缺失)。
    *   `created_at` (DateTime): 缺失建立時間。
    *   `status` (String): 缺失狀態 (e.g., "等待中", "改善中", "待確認", "已完成", "退件")。
    *   `confirmer_id` (Integer, Foreign Key to `users`): 確認者識別碼。
*   **關係**:
    *   多對一 (`project`): 多個缺失屬於一個專案。
    *   多對一 (`submitter`): 多個缺失由一個使用者提交。
    *   多對一 (`category`): 多個缺失屬於一個缺失類別。
    *   多對一 (`assigned_vendor`): 多個缺失指派給一個廠商。
    *   多對一 (`responsible_vendor`): 多個缺失由一個廠商負責。
    *   多對一 (`previous_defect`): 缺失可以有一個前置缺失。
    *   一對多 (`defect_marks`): 一個缺失可以有多個標記。
    *   一對多 (`improvements`): 一個缺失可以有多個改善記錄。

#### 8. `defect_marks` (缺失標記)

*   **描述**: 儲存缺失在基礎地圖上的位置標記。
*   **欄位**:
    *   `defect_mark_id` (Integer, Primary Key): 缺失標記唯一識別碼。
    *   `defect_id` (Integer, Foreign Key to `defects`): 缺失識別碼。
    *   `base_map_id` (Integer, Foreign Key to `base_maps`): 基礎地圖識別碼。
    *   `coordinate_x` (Float): 標記在基礎地圖上的 X 座標。
    *   `coordinate_y` (Float): 標記在基礎地圖上的 Y 座標。
    *   `scale` (Float): 標記的比例。
*   **關係**:
    *   多對一 (`defect`): 多個缺失標記屬於一個缺失。
    *   多對一 (`base_map`): 多個缺失標記位於一個基礎地圖上。

#### 9. `photos` (照片)

*   **描述**: 儲存與缺失、改善或確認單相關的照片資訊。
*   **欄位**:
    *   `photo_id` (Integer, Primary Key): 照片唯一識別碼。
    *   `related_type` (String): 關聯類型 (e.g., "defect", "improvement", "confirmation")。
    *   `related_id` (Integer): 關聯實體的識別碼。
    *   `description` (Text): 照片描述。
    *   `image_url` (String): 照片圖片檔案路徑。
    *   `created_at` (DateTime): 照片上傳時間。
*   **關係**:
    *   無直接外鍵關係，透過 `related_type` 和 `related_id` 邏輯關聯 `defects`, `improvements`, `confirmations`。

#### 10. `improvements` (改善)

*   **描述**: 儲存針對缺失所做的改善記錄。
*   **欄位**:
    *   `improvement_id` (Integer, Primary Key): 改善記錄唯一識別碼。
    *   `defect_id` (Integer, Foreign Key to `defects`): 相關缺失識別碼。
    *   `submitter_id` (Integer, Foreign Key to `users`): 改善提交者識別碼。
    *   `content` (Text): 改善內容描述。
    *   `improvement_date` (String): 改善日期。
    *   `created_at` (DateTime): 改善記錄建立時間。
*   **關係**:
    *   多對一 (`defect`): 多個改善記錄屬於一個缺失。
    *   多對一 (`submitter`): 多個改善記錄由一個使用者提交。
    *   一對多 (`confirmations`): 一個改善記錄可以有多個確認。

#### 11. `confirmations` (確認)

*   **描述**: 儲存針對改善的確認記錄。
*   **欄位**:
    *   `confirmation_id` (Integer, Primary Key): 確認記錄唯一識別碼。
    *   `improvement_id` (Integer, Foreign Key to `improvements`): 相關改善記錄識別碼。
    *   `confirmer_id` (Integer, Foreign Key to `users`): 確認者識別碼。
    *   `comment` (Text): 確認意見。
    *   `confirmation_date` (String): 確認日期。
    *   `status` (String): 確認狀態 (e.g., "接受", "退回", "未確認")。
    *   `created_at` (DateTime): 確認記錄建立時間。
*   **關係**:
    *   多對一 (`improvement`): 多個確認記錄屬於一個改善。
    *   多對一 (`confirmer`): 多個確認記錄由一個使用者進行。

### 關係圖 (Conceptual Relationship Diagram)

以下是各主要資料表之間關係的文字表示，類似於實體關係圖 (ERD) 的概念：

```
+-----------------+       +-----------------+       +-------------------+
|     projects    |       |      users      |       |    defect_categories  |
+-----------------+       +-----------------+       +-------------------+
| project_id (PK) |<----o-| user_id (PK)    |       | defect_category_id (PK)|
| project_name    |       | line_id         |       | project_id (FK)   |
| ...             |       | name            |       | category_name     |
+-----------------+       | email           |       | ...               |
        |                 | ...             |       +-------------------+
        |                 +-----------------+                 |
        |                                                     |
        | 1                                                   | 1
        |                                                     |
        o<----------------------------------------------------o
        |                                                     |
        | N                                                   | N
        |                                                     |
+-----------------+       +-----------------+       +-----------------+
|   permissions   |       |    vendors      |       |    base_maps    |
+-----------------+       +-----------------+       +-----------------+
| permission_id(PK)|       | vendor_id (PK)  |       | base_map_id (PK)|
| project_id (FK) |<----o-| project_id (FK) |<----o-| project_id (FK) |
| user_email      |       | vendor_name     |       | map_name        |
| user_role       |       | ...             |       | ...             |
+-----------------+       +-----------------+       +-----------------+
        |                         |                         |
        |                         |                         |
        | 1                       | 1                       | 1
        |                         |                         |
        o<------------------------o<------------------------o
        |                         |                         |
        | N                       | N                       | N
        |                         |                         |
+-----------------+       +-----------------+       +-----------------+
|     defects     |       |  defect_marks   |       |    photos       |
+-----------------+       +-----------------+       +-----------------+
| defect_id (PK)  |<----o-| defect_mark_id(PK)|       | photo_id (PK)   |
| project_id (FK) |       | defect_id (FK)  |       | related_type    |
| submitted_id (FK)|       | base_map_id (FK)|       | related_id      |
| defect_category_id (FK)| | coordinate_x    |       | ...             |
| assigned_vendor_id (FK)| | coordinate_y    |       +-----------------+
| responsible_vendor_id (FK)| | scale           |
| previous_defect_id (FK)| +-----------------+
| confirmer_id (FK)|
| ...             |
+-----------------+
        |
        | 1
        |
        o<------------------------------------------------------------------+
        |                                                                 |
        | N                                                                 |
        |                                                                 |
+-----------------+       +-----------------+       +-----------------+
|   improvements  |       |  confirmations  |       | (logical link)  |
+-----------------+       +-----------------+       | (photos to defects, |
| improvement_id(PK)|<----o-| confirmation_id(PK)|       | improvements, confirmations) |
| defect_id (FK)  |       | improvement_id(FK)|       +-----------------+
| submitter_id (FK)|       | confirmer_id (FK)|
| ...             |       | ...             |
+-----------------+       +-----------------+
```

**圖例說明**:
*   `PK`: Primary Key (主鍵)
*   `FK`: Foreign Key (外鍵)
*   `o--<`: 一對多關係 (One-to-Many), `o` 在「一」的一方，`<` 在「多」的一方。
*   `N`: 表示「多」的一方。
*   `1`: 表示「一」的一方。
*   `logical link`: 表示在資料庫層面沒有直接的外鍵約束，但應用程式邏輯上存在關聯。

### 關係總結 (Relationship Summary)

*   **專案 (Projects)** 是核心，所有其他實體（使用者權限、廠商、缺失類別、基礎地圖、缺失）都直接或間接與專案關聯。
*   **使用者 (Users)** 可以提交缺失和改善，並進行確認。
*   **權限 (Permissions)** 定義了使用者在特定專案中的角色，但 `user_email` 欄位在資料庫層面並非外鍵，而是透過應用程式邏輯與 `users.email` 關聯。
*   **廠商 (Vendors)** 屬於特定專案，並可被指派為缺失的負責方或指派方。
*   **缺失類別 (Defect Categories)** 屬於特定專案，用於分類缺失。
*   **基礎地圖 (Base Maps)** 屬於特定專案，是缺失標記的載體。
*   **缺失 (Defects)** 是系統的核心業務實體，與專案、提交者、類別、廠商、前置缺失等都有關聯。
*   **缺失標記 (Defect Marks)** 將缺失與基礎地圖上的具體位置關聯起來。
*   **照片 (Photos)** 是一個通用表，可以關聯到缺失、改善或確認單，但這種關聯是透過 `related_type` 和 `related_id` 欄位在應用程式層面實現的，而非資料庫外鍵。
*   **改善 (Improvements)** 針對特定的缺失，由使用者提交。
*   **確認 (Confirmations)** 針對特定的改善，由使用者進行，並會影響相關缺失的狀態。

這個詳細的說明應該能幫助您更全面地理解後端缺陷管理系統的資料結構和模組間的互動。