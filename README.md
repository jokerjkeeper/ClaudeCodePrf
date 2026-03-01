# ClaudeCodePrf

**Claude Code 工作流配置模板** — 一鍵安裝，讓 Claude Code 在任何專案中遵守統一的開發規範。

---

## 功能特色

- **全局基礎配置** — Session 管理、權限分級、代碼規範、Excalidraw 架構圖輸出
- **4 種專案 Profile** — PHP / Python Web / Unity / Obsidian 各有專屬規範
- **13 個自定義 Commands** — 進度追蹤、Code Review、角色切換等
- **Apify 爬蟲集成** — MCP Server + Skill，一鍵配置網頁爬蟲能力

---

## 一鍵安裝

```bash
# 1. Clone 本 repo
git clone https://github.com/your-username/ClaudeCodePrf.git

# 2. 執行安裝腳本
cd ClaudeCodePrf
bash setup.sh
```

腳本會引導你完成：
1. 設定目標專案路徑
2. 選擇專案類型 (Profile)
3. 選擇要啟用的 Commands
4. 是否啟用 Apify 爬蟲功能
5. 自動安裝所有配置文件

---

## 專案 Profile

| Profile | 文件 | 適用場景 |
|---------|------|----------|
| PHP | `claude_php.md` | Laravel 11 + Vue 3 + Tailwind，含 RBAC、三端適配 |
| Python Web | `claude_pyweb.md` | FastAPI / Django，含 SQLAlchemy、Pydantic、pytest |
| Unity | `claude_unity.md` | Unity 2022.3 LTS，C# 規範、Log 分析、Package 管理 |
| Obsidian | `claude_obsi.md` | Obsidian Vault 管理、Dataview 查詢、任務篩選 |

---

## Commands 速查表

### 核心 Commands

| 命令 | 說明 |
|------|------|
| `/save` | 保存當前 Session 進度到 `.claude/session.md` |
| `/resume` | 讀取並恢復上次 Session 進度 |
| `/task` | 將目前項目進度記錄到 task list |
| `/path` | 打印目前工作目錄完整路徑 |
| `/report` | 生成專案狀態報告（進度、問題、建議） |
| `/review` | 對最近修改的文件進行 Code Review |
| `/role {角色}` | 切換到指定角色口吻（如：科學家、產品經理） |

### 進階 Commands

| 命令 | 說明 |
|------|------|
| `/architecture` | 分析專案結構，輸出 Excalidraw 兼容的架構圖 |
| `/export-math` | 將 Session 中使用的數學模型匯出到 `.claude/math.md` |
| `/load-math` | 載入 `.claude/math.md` 中的數學模型作為上下文 |

### Obsidian Commands

| 命令 | 說明 |
|------|------|
| `/obs-pdf` | 將 Obsidian Markdown 檔案轉換為 PDF |
| `/obs-todo` | 篩選並顯示未完成任務 |
| `/obs-plt` | 篩選並顯示已完成任務 |

---

## 手動安裝

如果不使用安裝腳本，可以手動複製文件：

```bash
# 1. 複製基礎配置
cp CLAUDE.md /path/to/your/project/

# 2. 複製 Profile（以 PHP 為例）
cp claude_php.md /path/to/your/project/

# 3. 在 CLAUDE.md 末尾加入載入指令
echo '請同時讀取並遵守 claude_php.md 中的所有規則。' >> /path/to/your/project/CLAUDE.md

# 4. 建立目錄結構
mkdir -p /path/to/your/project/.claude/commands

# 5. 複製 Commands
cp .claude/commands/*.md /path/to/your/project/.claude/commands/

# 6. 初始化 Session 記錄
cp templates/session.md /path/to/your/project/.claude/session.md
```

---

## 目錄結構

### 本 Repo 結構

```
ClaudeCodePrf/
├── setup.sh                    # 交互式安裝腳本
├── CLAUDE.md                   # 全局基礎配置
├── claude_php.md               # PHP Profile
├── claude_pyweb.md             # Python Web Profile
├── claude_unity.md             # Unity Profile
├── claude_obsi.md              # Obsidian Profile
├── .claude/
│   ├── .env.sample             # 環境變數模板 (Apify Token)
│   └── commands/               # 13 個自定義命令
│       ├── save.md
│       ├── resume.md
│       ├── task.md
│       ├── path.md
│       ├── report.md
│       ├── review.md
│       ├── role.md
│       ├── architecture.md
│       ├── export-math.md
│       ├── load-math.md
│       ├── obs-pdf.md
│       ├── obs-todo.md
│       └── obs-plt.md
├── apify-skills/               # Apify Skill 模板
│   └── apify-ultimate-scraper.md
└── templates/                  # 安裝用模板文件
    ├── session.md
    └── settings.apify.json
```

### 安裝後的目標專案結構

```
your-project/
├── CLAUDE.md                      # 全局規則
├── claude_<type>.md               # 專案 Profile
├── .claude/
│   ├── session.md                 # 進度記錄
│   ├── commands/                  # 自定義命令
│   │   ├── save.md
│   │   └── ...
│   ├── skills/                    # Apify Skill (可選)
│   ├── settings.local.json        # MCP 配置 (可選)
│   └── .env.sample                # 環境變數模板 (可選)
└── ...
```

---

## Apify 爬蟲配置

啟用 Apify 後，安裝腳本會自動建立：

- `.claude/skills/apify-ultimate-scraper.md` — Skill 定義文件
- `.claude/settings.local.json` — MCP Server 配置
- `.claude/.env.sample` — 填入你的 `APIFY_TOKEN`

使用前需要：
1. 註冊 [Apify](https://apify.com/) 帳號
2. 取得 API Token
3. 填入 `.claude/.env.sample` 中的 `APIFY_TOKEN`

---

## License

MIT
