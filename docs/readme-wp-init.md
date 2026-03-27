# WePages 工單連線初始化指南

讓 Claude Code 的每個項目都能自動連線 WePages 工單系統，跨機器同步、零配置啟動。

---

## 架構概覽

```
your-project/
└── .claude/
    ├── api.conf                              # Token + URL + 工單ID
    ├── commands/
    │   └── wp-init.md                        # 初始化指令（可複製到其他項目）
    ├── claude_specs/
    │   └── claude_spc_wepages.md             # API 參考文檔（SessionStart 自動載入）
    ├── scripts/
    │   └── load-specs.sh                     # 規格文件載入腳本
    └── settings.local.json                   # SessionStart hook 設定
```

**運作原理：**

1. 新 session 啟動 → SessionStart hook 觸發
2. `load-specs.sh` 載入 `claude_specs/` 下所有 `.md` → Claude 知道有工單 API
3. hook 輸出 `api.conf` 內容 → Claude 拿到 Token 和工單 ID
4. 你說「查工單」→ Claude 直接用 curl 操作

---

## 首次設定（當前項目）

### 1. 執行初始化指令

在 Claude Code 中輸入：

```
/wp-init #50
```

或提供完整參數：

```
/wp-init #50 http://127.0.0.1:5002 wep_your_token_here
```

### 2. 初始化會自動完成以下工作

| 步驟 | 產出檔案 | 說明 |
|------|---------|------|
| 建立設定檔 | `.claude/api.conf` | 存放 Token、URL、工單 ID |
| 建立 API 參考 | `.claude/claude_specs/claude_spc_wepages.md` | 端點文檔，自動載入 |
| 更新 Hook | `.claude/settings.local.json` | SessionStart 自動輸出設定 |

### 3. 提交到 git

```bash
git add .claude/api.conf .claude/claude_specs/claude_spc_wepages.md .claude/commands/wp-init.md .claude/settings.local.json
git commit -m "feat(.claude): add WePages ticket integration"
git push
```

> **注意：** `api.conf` 包含 API Token，請確認 repo 為 **private**。

### 4. 另一台電腦

```bash
git pull
```

下次開 Claude Code 就直接能用，不需要任何額外設定。

---

## 新項目初始化

### 方法一：複製 + 執行

1. 將 `wp-init.md` 複製到新項目：

```bash
cp /path/to/existing-project/.claude/commands/wp-init.md /path/to/new-project/.claude/commands/
```

2. 在新項目中開啟 Claude Code，執行：

```
/wp-init #工單ID
```

如果 Token 和 URL 與其他項目相同，只需提供工單 ID。

### 方法二：手動建立

如果不想用指令，手動建立以下檔案：

**`.claude/api.conf`**
```bash
# WePages API Config (committed to private repo)
WEPAGES_TOKEN=wep_your_token_here
WEPAGES_URL=http://127.0.0.1:5002
WEPAGES_TASK_ID=63
```

**`.claude/settings.local.json`** 中的 SessionStart hook 需包含：
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "if [ -f .claude/api.conf ]; then cat .claude/api.conf | grep -v '^#' | grep '=' ; fi",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

---

## 日常使用

初始化完成後，在 Claude Code 中用自然語言操作即可：

| 你說的話 | Claude 做的事 |
|---------|-------------|
| 「查工單」 | 讀取綁定工單的詳情與子清單 |
| 「更新進度到 40%」 | 呼叫 API 更新 progress |
| 「加一條備注：今天完成了 X」 | 呼叫 API 新增 note |
| 「勾選 XXX」 | 找到對應子清單項目並 toggle |
| 「新增子清單：項目A, 項目B」 | 批次新增 checklist items |
| 「比對工單跟本地進度」 | 讀取工單 + session.md，列出差異 |

---

## 檔案說明

### `.claude/api.conf`

```bash
WEPAGES_TOKEN=wep_xxx          # API 認證 Token
WEPAGES_URL=http://127.0.0.1:5002  # WePages 服務地址
WEPAGES_TASK_ID=50             # 本項目綁定的主工單 ID
```

- 省略工單 ID 時，Claude 會使用 `WEPAGES_TASK_ID` 作為預設值
- 一個項目綁定一個主工單

### `.claude/claude_specs/claude_spc_wepages.md`

API 端點參考文檔，包含：
- 連線方式與 curl 格式
- 所有 task / checklist 端點
- 欄位可選值（status、priority、task_type）

此檔案被 `load-specs.sh` 在 SessionStart 時自動載入，Claude 每次新 session 都會讀到。

### `.claude/commands/wp-init.md`

初始化指令定義。可複製到任何項目使用。

---

## 與 /wp skill 的關係

| | `/wp-init` | `/wp` |
|---|-----------|-------|
| 用途 | Claude Code 本地初始化 | Discord robot agent |
| 連線方式 | curl + REST API | MCP tools |
| 使用者 | 開發者（你） | Discord bot |
| 位置 | `.claude/commands/wp-init.md` | `.claude/commands/wp.md` |

兩者互不干擾。`/wp-init` 不會修改 `/wp`。

---

## FAQ

**Q: 換了 Token 怎麼辦？**
A: 直接修改 `.claude/api.conf` 中的 `WEPAGES_TOKEN`，commit + push。

**Q: 想綁定不同工單？**
A: 修改 `WEPAGES_TASK_ID`，或重新執行 `/wp-init #新ID`。

**Q: WePages 服務沒啟動怎麼辦？**
A: Claude 會在第一次 curl 時發現 ECONNREFUSED 並提醒你啟動服務。配置檔不受影響。

**Q: 可以同時操作多個工單嗎？**
A: 可以。`WEPAGES_TASK_ID` 只是預設值，你隨時可以指定其他 ID：「查工單 #63」。
