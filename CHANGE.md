# 變更日誌

## [日期]

### 重構

*   **重構使用者模組測試程式碼**
    *   將多個使用者相關的測試檔案 (`test_user_avatar.py`, `test_user_project_relation.py`, `test_user_update_edge_cases.py`, `test_user_validation.py`) 合併至 `test_user.py`。
    *   此舉旨在簡化測試結構，將所有使用者相關的測試集中管理，提高可維護性。

### 清理

*   **移除已棄用及註解的測試程式碼**
    *   刪除了 `test_defect.py` 中已棄用的 `test_get_defect_with_marks_and_photos` 測試。
    *   清除了 `test_permission.py`, `test_photo.py`, 和 `test_project.py` 中被註解掉的無用測試程式碼。
    *   放寬了部分 `test_user.py` 中的斷言條件，使其更具彈性。
