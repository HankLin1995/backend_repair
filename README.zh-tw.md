# 後端缺失管理系統

這是一個使用 FastAPI 建置的綜合性缺失管理系統後端。它提供了一個強大的 API，用於管理專案、使用者、缺失、廠商及相關數據，適用於營造、製造和品保等行業。

## 主要功能

- **專案管理**：對專案進行 CRUD 操作，包括專案圖片上傳。
- **使用者管理**：使用者註冊、個人資料更新和頭像管理。
- **基於角色的存取控制**：為每個專案的使用者分配角色（如管理員、編輯者、檢視者）。
- **缺失追蹤**：詳細的缺失記錄，包括位置、描述、狀態追蹤和照片附件。
- **廠商管理**：管理廠商資訊並將其分配給特定的缺失。
- **改善與確認週期**：追蹤改善建議及其確認狀態。
- **檔案上傳**：處理專案視覺、使用者頭像和缺失照片的圖片上傳。
- **數據關聯**：專案、使用者、缺失和廠商之間有明確定義的關聯。
- **統計分析**：提供取得缺失分佈和狀態統計數據的端點。

## 使用技術

- **後端**：Python, FastAPI
- **資料庫**：SQLAlchemy ORM (相容於 PostgreSQL, SQLite 等)
- **測試**：Pytest
- **容器化**：Docker, Docker Compose

## 專案結構

本專案採用模組化結構，每個主要功能區塊都放在 `app/` 下的獨立目錄中。

```
app/
├───base_map/         # 底圖管理
├───confirmation/     # 改善的確認記錄
├───defect/           # 核心缺失追蹤邏輯
├───defect_category/  # 缺失分類
├───defect_mark/      # 缺失照片/地圖上的標記
├───improvement/      # 改善建議
├───permission/       # 使用者-專案權限
├───photo/            # 照片處理
├───project/          # 專案管理
├───user/             # 使用者管理
├───vendor/           # 廠商管理
├───database.py       # 資料庫會話設定
├───main.py           # FastAPI 應用程式進入點
└───tests/            # Pytest 測試套件
```

## 安裝與設定

1.  **複製儲存庫：**
    ```bash
    git clone <repository-url>
    cd backend_defect
    ```

2.  **建立並啟用虛擬環境：**
    - 在 Windows 上：
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```
    - 在 macOS/Linux 上：
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3.  **安裝依賴套件：**
    ```bash
    pip install -r requirements.txt
    ```

## 執行應用程式

若要執行開發伺服器，請使用 `uvicorn`：

```bash
uvicorn app.main:app --reload
```

API 將在 `http://127.0.0.1:8000` 上提供，而互動式 API 文件 (Swagger UI) 可在 `http://127.0.0.1:8000/docs` 存取。

## 執行測試

本專案使用 `pytest` 進行測試。若要執行整個測試套件：

```bash
pytest
```

## 資料庫

資料庫結構定義在 `database.dbml` 檔案中，使用 DBML。對應此結構的 SQLAlchemy 模型位於每個功能模組的 `models.py` 檔案中（例如 `app/user/models.py`）。
