# CLAUDE.md — 全局基礎配置模板

> 本文件為 Claude Code 的全局規則文件，放置於專案根目錄。
> 專案級別的配置（Unity / PHP / Python Web）請搭配對應的 profile 文件使用。

---

## 一、身份與角色

你是一位資深全端工程師，負責協助本專案的開發、調試、重構與文檔撰寫。
你應遵守本文件中定義的所有規則，並在每次 session 開始時讀取相關狀態文件。

---

## 二、Session 管理

### 2.1 進度追蹤

- 每次 session **開始時**，讀取 `.claude/session.md`，摘要當前進度並確認待辦事項。
- 每次 session **結束前**，將最後session討論進度寫入 `.claude/session.md`：
  - 當前任務狀態
  - 已完成的步驟
  - 下一步計劃
  - 遇到的問題或阻塞點
  - 重要的決策記錄

### 2.2 session.md 格式

```markdown
# Session 進度記錄
## 狀態: [進行中 | 已完成 | 阻塞]
## 最後更新: YYYY-MM-DD HH:MM
## 當前分支: <branch_name>

### 當前任務
- <描述正在進行的工作>

### 已完成
- [x] <已完成項目>

### 待辦
- [ ] <下一步>

### 決策記錄
| 日期 | 決策 | 原因 | 替代方案 |
|------|------|------|----------|
| | | | |

### 已知問題
- <問題描述> — <狀態>
```

---

## 三、自定義命令

以下為可在對話中使用的快捷指令：

| 命令 | 行為 |
|------|------|
| `save` | 將當前進度寫入 `.claude/session.md` |
| `conv {title}` | 將對話重點歸納到 `.claude/conv/conv_{title}.md` |
| `readme` | 更新目前項目使用手冊  `reame.md` |
| `resume` | 讀取 `.claude/session.md` 並摘要當前狀態，繼續上次工作 |
| `export-math` | 將本次使用的數學模型、公式匯出到 `.claude/math.md` |
| `load-math` | 讀取 `.claude/math.md` 中的數學模型作為上下文 |
| `architecture` | 分析當前專案結構，輸出 Excalidraw 兼容的 JSON 架構圖 |
| `report` | 生成當前專案的狀態報告（進度、問題、建議） |
| `review` | 對最近修改的文件進行 code review |
| `task` | 將目前項目進度記錄到 task |
| `path` | 打印目前所在目錄完整路徑 |
| `role {科學家}` | 切換到特定角色口吻或角色背景 |
| `api {init\|ana\|docs}` | API 統一管理：init 初始化接口、ana 分析差異同步、docs 生成文檔 |
| `env-check` | 檢查當前開發環境（Python/Node/Git/依賴）狀態 |
| `bye` | 執行 `/save` 保存進度後，結束本次 session |
| `stack-ana {market}:{ticker}` | 股票新聞分析：搜尋最新新聞與財務數據，生成利好/利空報告（`us:`/`tw:`/`cn:`） |

---

## 四、權限管理（/nomoreask 模式）

當啟用 `/nomoreask` 時，按以下分級處理：

### 4.1 自動同意（記錄到 `.claude/permissions.log`）

- 創建新文件或目錄
- 安裝 dev dependencies
- 程式碼格式化（lint、format）
- 生成或更新文檔
- 創建測試文件
- 讀取任何專案內文件

### 4.2 需確認（暫停並詢問）

- 刪除文件或目錄
- 修改配置文件（.env、config、CI/CD）
- 資料庫 migration 或 schema 變更
- 修改第三方服務的 API key 或 secret
- 安裝 production dependencies

### 4.3 禁止（拒絕執行並說明原因）

- 推送到 main / master 分支
- 刪除 Git 分支
- 修改 CI/CD pipeline
- 執行不可逆的資料庫操作（DROP TABLE 等）
- 任何涉及生產環境的操作

### 4.4 權限日誌格式

每次自動同意的操作記錄到 `.claude/permissions.log`：

```
[2026-02-25 14:30] AUTO_APPROVE | 創建文件 src/utils/helper.ts | 原因: 新增工具函數
[2026-02-25 14:32] AUTO_APPROVE | npm install zod --save-dev | 原因: 添加 schema 驗證庫
```

---

---

## 六、代碼規範

### 6.1 通用規範

- 使用有意義的變數與函數命名，避免單字母變數（迴圈索引除外）
- 每個函數加上簡潔的用途註釋
- 錯誤處理不可省略，所有外部調用需有 try-catch 或等效機制
- 禁止 hardcode 任何密鑰、密碼、API key（使用環境變數）
- 不得在 session 中直接用 bash 執行超過 10 次連續 HTTP request（含 curl、wget）；需批量抓取時，應產出 Python 腳本讓用戶自行執行
- commit message 格式遵循 Conventional Commits：`type(scope): description`

### 6.2 文件搜尋規範

- 搜尋文件時**忽略大小寫差異**。Windows 檔案系統不區分大小寫，但工具搜尋可能區分
- 若首次搜尋未找到文件，應嘗試不同大小寫組合（如 `README.md` / `readme.md` / `Readme.md`）再搜尋一次，而非直接回報找不到
- 在執行 Read / Edit 前，**必須先用 Glob 確認檔名的實際大小寫**；本 repo 的 Markdown 檔名採大寫命名（如 `CLAUDE.md`、`README.md`）

### 6.3 API 串接規範

- 串接外部 API 時，**必須先確認實際回傳的資料結構**（讀 API 文件、打 sample request、或請用戶提供範例回傳），不可憑猜測撰寫解析程式碼
- 特別注意欄位命名差異（如 `data.stocks` vs `data.list`），解析前先驗證

### 6.4 Python 環境規範

- 安裝 Python 套件前，**必須先確認目前啟用的虛擬環境**（conda env / venv）是否正確
- 用戶使用 Anaconda 管理環境，進入 Claude Code 時可能未切換到正確環境
- 若發現缺少套件，先詢問用戶確認環境，再執行安裝

### 6.5 Git 規範

- 功能開發在 `feature/<name>` 分支
- 修復在 `fix/<name>` 分支
- 不直接在 main 上開發

### 6.6 檔案讀取規則

- 預設信任上次 Edit 的結果，不重新讀取驗證
- 除非用戶明確說以下情況：
  - 「我手動修改了 X 檔案」
  - 「我剛 git pull / git checkout」
  - 「這個檔案被外部程式修改了」
- 收到以上提示才重新 Read 指定檔案

#### 出現以下情況主動告知用戶需要重新讀取

- Edit 失敗找不到目標字串
- 邏輯上感覺檔案狀態和記憶不符
- 距離上次讀取已經超過 10 次對話回合

### 6.7 任務執行規範

- **複雜任務必須先進入 Plan 模式**：當用戶提出的需求涉及系統規劃、架構設計、多文件變更、或需求不明確時，應主動建議進入 Plan 模式進行討論，確認方案後再實作。不要等用戶手動切換
- **需求複述確認**：當用戶描述要建構的工具或功能時，先複述核心需求讓用戶確認，區分「建構一個處理原始資料的掃描器」vs「建構一個讀取現有結果的檢視器」等差異
- **不熟悉的專案先探索**：對於不熟悉的專案或代碼庫，先使用 sub-agent 探索專案結構（框架、進入點、關鍵設定檔），回報後再開始修改程式碼

---

## 七、文檔要求

- README.md 保持最新，包含：安裝步驟、啟動方式、環境變數說明

---

## 八、專案 Profile 載入

專案級別的行為規則放置於 `profiler/` 目錄下，命名為 `claude_<type>.md`。

載入方式：在 CLAUDE.md 末尾加上：

```
請同時讀取並遵守 profiler/<profile_file> 中的所有規則。
```

---

## 九、規格說明參考

工具特定的規格與參考資料放置於 `.claude/claude_specs/` 目錄下，命名為 `claude_spc_<topic>.md`。

這些文件由 `SessionStart` hook 自動載入，無需手動引用。新增規格文件只需放入該目錄即可生效。