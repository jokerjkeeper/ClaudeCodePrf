# WePages 工單管理

統一操作 WePages 工單系統的快捷指令。根據參數自動判斷操作類型。

## 參數格式

`/wp <操作> [工單ID] [附加內容]`

## 操作類型

### 1. 查詢工單：`/wp list` 或 `/wp #ID`

- `/wp list` — 列出所有進行中的工單（status: in_progress）
- `/wp list all` — 列出所有未完成工單（pending + in_progress + reviewing）
- `/wp list 關鍵字` — 搜尋工單
- `/wp #63` — 查看指定工單的詳細資訊與子清單

**執行：** 使用 `mcp__wepages-tasks__list_tasks` 或 `mcp__wepages-tasks__get_task`，呈現工單資訊。

---

### 2. 開始處理工單：`/wp start #ID`

- 將工單狀態更新為 `in_progress`
- 讀取工單詳情與子清單，摘要待辦事項
- 如有子清單，列出未完成項目

**執行：**
1. `mcp__wepages-tasks__get_task` 取得工單詳情
2. `mcp__wepages-tasks__update_task` 更新狀態為 `in_progress`
3. 向用戶摘要工單內容，確認開始工作

---

### 3. 更新為待驗收：`/wp review #ID`

- 將工單狀態更新為 `reviewing`
- 自動回顧本次 session 的工作內容，新增進度備注
- 列出子清單完成狀況

**執行：**
1. `mcp__wepages-tasks__get_task` 取得當前狀態
2. `mcp__wepages-tasks__add_task_note` 新增本次工作摘要備注
3. `mcp__wepages-tasks__update_task` 更新狀態為 `reviewing`
4. 向用戶確認已提交驗收

---

### 4. 更新為完成：`/wp done #ID`

- 將工單狀態更新為 `completed`，進度設為 100
- 新增完成備注（包含最終變更摘要）

**執行：**
1. `mcp__wepages-tasks__get_task` 取得當前狀態
2. `mcp__wepages-tasks__add_task_note` 新增完成摘要
3. `mcp__wepages-tasks__update_task` 更新狀態為 `completed`，進度 100
4. 向用戶確認工單已關閉

---

### 5. 新增備注：`/wp note #ID 備注內容`

- 將指定內容新增到工單的進度備注
- 如未提供備注內容，則自動回顧本次 session 對話，整理修正內容作為備注
- 可選附帶進度更新：`/wp note #63 修正完成 80`（最後的數字為進度百分比）

**執行：**
1. 解析備注內容與可選的進度數字
2. `mcp__wepages-tasks__add_task_note` 新增備注（如有進度數字則同時更新進度）
3. 向用戶確認備注已新增

---

### 6. 更新子清單：`/wp check #ID`

- 查看指定工單的子清單狀態
- `/wp check #ID #項目ID` — 勾選/取消勾選指定子清單項目
- `/wp check #ID all` — 根據本次 session 的工作內容，自動識別已完成的子清單項目並勾選
- `/wp check #ID add 項目1, 項目2` — 批次新增子清單項目

**執行：**
- 查看：`mcp__wepages-tasks__get_checklist`
- 勾選：`mcp__wepages-tasks__toggle_checklist_item`
- 新增：`mcp__wepages-tasks__add_checklist_items`
- 自動識別：回顧對話內容，比對子清單項目，批次勾選已完成的項目

---

## 省略工單 ID 的行為

如果操作需要工單 ID 但未提供：
1. 先檢查本次 session 是否有正在處理的工單（從對話上下文推斷）
2. 如果有，自動使用該工單 ID
3. 如果沒有，列出所有進行中的工單讓用戶選擇

## 範例

```
/wp list              → 列出進行中工單
/wp #63               → 查看工單 #63 詳情
/wp start #63         → 開始處理工單 #63
/wp note #63          → 自動整理本次工作內容作為備注
/wp note #63 修正 DLC 模組 80  → 新增備注並更新進度到 80%
/wp check #63         → 查看子清單
/wp check #63 #44     → 勾選子清單項目 #44
/wp check #63 add 新增測試, 修正文件  → 新增子清單項目
/wp review #63        → 提交驗收
/wp done #63          → 標記完成
```
