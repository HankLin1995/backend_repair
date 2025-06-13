import os
from sqlalchemy.orm import Session
from app.project import crud
from app.base_map.models import BaseMap

def delete_project_with_files(db: Session, project_id: int) -> bool:
    """
    刪除 project 前，先刪除所有 base_map 的圖片檔案，再刪除 project。
    """
    # 查詢所有 base_map 的 file_path
    base_maps = db.query(BaseMap).filter(BaseMap.project_id == project_id).all()
    for base_map in base_maps:
        file_path = base_map.file_path
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                # 可以根據需求記錄 log 或忽略
                pass
    # 刪除 project（cascade 會自動刪 base_map 資料）
    return crud.delete_project(db, project_id)
