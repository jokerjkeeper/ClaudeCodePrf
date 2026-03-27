# wp-init — 初始化項目工單連線

將當前項目與 WePages 工單系統建立連線。執行後，該項目的每次 Claude Code session 都能自動存取工單 API。

## 使用方式

```
/wp-init                                          → 互動式詢問所有資訊
/wp-init #50                                      → 指定工單 ID，其餘互動詢問
/wp-init #50 http://127.0.0.1:5002 wep_xxx        → 一次提供所有資訊
```

## 執行流程

### Step 1：收集資訊

向用戶詢問以下資訊（如已在參數中提供則跳過）：

| 欄位 | 說明 | 預設值 |
|------|------|--------|
| WePages URL | 服務地址 | `http://127.0.0.1:5002` |
| API Token | 認證 Token | （必填） |
| 工單 ID | 要綁定的主工單編號 | （必填） |

如果當前項目已有 `.claude/api.conf`，讀取其中的 URL 和 Token 作為預設值，只詢問工單 ID。

### Step 2：驗證連線

```bash
source .claude/api.conf
curl -s "$WEPAGES_URL/api/task/get?id=$WEPAGES_TASK_ID" -H "Authorization: Bearer $WEPAGES_TOKEN"
```

- 返回工單資料 → 連線成功，繼續
- 返回 Unauthorized → Token 錯誤，請用戶重新提供
- ECONNREFUSED → 服務未啟動，提醒用戶，但仍可繼續建立配置

### Step 3：建立 `.claude/api.conf`

```bash
# WePages API Config (committed to private repo)
WEPAGES_TOKEN=<token>
WEPAGES_URL=<url>
WEPAGES_TASK_ID=<task_id>
```

### Step 4：建立 `.claude/claude_specs/claude_spc_wepages.md`

建立 WePages API 參考文檔，內容包含：
- 連線方式（source api.conf + curl 格式）
- 常用 API 端點表（task get/list/update/complete、checklist add/toggle/list）
- 任務欄位說明（status/priority/task_type 的可選值）
- 注意事項（/wp skill 是 Discord robot 用的不要改、省略 ID 時用預設值）

此檔案會被 SessionStart hook 的 `load-specs.sh` 自動載入。

### Step 5：更新 SessionStart hook

讀取 `.claude/settings.local.json`，在 `hooks.SessionStart` 中追加（如尚未存在）：

```json
{
  "type": "command",
  "command": "if [ -f .claude/api.conf ]; then cat .claude/api.conf | grep -v '^#' | grep '=' ; fi",
  "timeout": 5
}
```

不覆蓋現有 hooks，僅追加。已存在則跳過。

如果 `settings.local.json` 不存在，建立基本結構：
```json
{
  "permissions": { "allow": [] },
  "hooks": { "SessionStart": [{ "hooks": [] }] }
}
```

同時確認 `load-specs.sh` 存在，如不存在則建立（從本項目的版本複製）。

### Step 6：驗證 .gitignore

檢查 `.gitignore` 確認 `api.conf` 不會被忽略（檔名非 `.env`，通常不受影響）。
提醒用戶：api.conf 含 Token，確認 repo 是 private。

### Step 7：輸出摘要

```
WePages 工單連線已建立
  服務：<url>
  綁定工單：#<id> <工單標題>
  配置檔：.claude/api.conf
  API 參考：.claude/claude_specs/claude_spc_wepages.md
  自動載入：SessionStart hook 已設定

下次新 session 啟動時會自動載入工單連線設定。
直接說「查工單」「更新進度」即可操作。
```

## 複製到其他項目

1. 將此檔案複製到新項目的 `.claude/commands/wp-init.md`
2. 在新項目中執行 `/wp-init #工單ID`
3. 如 Token 和 URL 相同，只需提供工單 ID，其餘從已有配置帶入

## 注意事項

- 一個項目綁定一個主工單，重複執行會覆蓋舊配置
- 所有配置檔都在項目 `.claude/` 目錄下，提交 git 後其他機器拉取即可使用
- `/wp` skill 是 Discord robot agent 用的 MCP 版本，wp-init 不會修改它
