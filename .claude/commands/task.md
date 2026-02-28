# Task Progress Tracking

將目前項目進度記錄到 task list，使用 TaskCreate / TaskUpdate 工具進行追蹤管理。

## 執行步驟

1. **收集當前狀態**
   - 讀取 `.claude/session.md`（如果存在），了解當前進度
   - 回顧本次 session 的對話內容，識別所有任務項目

2. **檢查現有 task**
   - 使用 `TaskList` 查看是否已有建立的任務
   - 避免建立重複的任務

3. **建立或更新 task**
   - 對每個識別到的任務，使用 `TaskCreate` 建立新任務，或使用 `TaskUpdate` 更新已有任務的狀態
   - 任務應包含：
     - **subject**: 簡潔的任務標題（祈使句形式，如「實作用戶登入功能」）
     - **description**: 詳細描述，包含上下文與驗收標準
     - **activeForm**: 進行中的現在進行式描述（如「實作用戶登入功能中」）
   - 根據實際進度設定正確的狀態：
     - `pending`: 尚未開始
     - `in_progress`: 進行中
     - `completed`: 已完成

4. **設定依賴關係**
   - 如果任務之間有先後順序，使用 `addBlocks` / `addBlockedBy` 建立依賴

5. **輸出摘要**
   - 列出所有建立/更新的任務及其狀態
   - 顯示整體進度概覽
