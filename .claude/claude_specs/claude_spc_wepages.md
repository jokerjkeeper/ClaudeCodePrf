# WePages 工單系統 — API 參考

本項目已連線 WePages 工單管理系統，可透過 REST API 操作工單。

## 連線設定

設定檔位於 `.claude/api.conf`，包含：
- `WEPAGES_TOKEN` — API 認證 Token
- `WEPAGES_URL` — 服務地址
- `WEPAGES_TASK_ID` — 本項目綁定的主工單 ID

使用前先載入：`source .claude/api.conf`

## 呼叫格式

```bash
curl -s "$WEPAGES_URL/<endpoint>" \
  -H "Authorization: Bearer $WEPAGES_TOKEN" \
  -H "Content-Type: application/json" \
  -d '<json_body>'
```

## 常用端點

| 操作 | 方法 | 路徑 | 參數 |
|------|------|------|------|
| 取得任務 | GET | `/api/task/get?id=<id>` | |
| 列出任務 | GET | `/api/task/list` | ?status=&q=&project_id=&limit= |
| 更新任務 | POST | `/api/task/update` | id, status, progress, note, tags |
| 完成任務 | POST | `/api/task/complete` | id |
| 子清單列表 | GET | `/api/task/checklist/list?task_id=<id>` | |
| 新增子清單 | POST | `/api/task/checklist/add` | task_id, items[] |
| 勾選子清單 | POST | `/api/task/checklist/toggle/<id>` | |
| 刪除子清單 | POST | `/api/task/checklist/delete/<id>` | |
| 列出項目 | GET | `/api/task/projects` | |

## 任務欄位

- status: `pending` / `in_progress` / `reviewing` / `completed` / `cancelled`
- priority: `low` / `medium` / `high` / `urgent`
- task_type: `bug` / `feature` / `discuss` / `optimize` / `other`
- note: 新增備注時傳入，會自動追加到備注列表

## 注意事項

- `/wp` skill（`.claude/commands/wp.md`）是給 Discord robot agent 使用的 MCP 版本，不要修改
- 本地 Claude Code session 中直接用 curl 操作即可
- 操作工單前建議先 `source .claude/api.conf` 載入環境變數
- 省略工單 ID 時，預設使用 `$WEPAGES_TASK_ID`（api.conf 中設定的主工單）
