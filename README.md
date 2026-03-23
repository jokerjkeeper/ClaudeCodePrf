# ClaudeCodePrf

**Claude Code 工作流配置模板** — 一鍵安裝，讓 Claude Code 在任何專案中遵守統一的開發規範。

---

## 功能特色

- **全局基礎配置** — Session 管理、權限分級、代碼規範、Excalidraw 架構圖輸出
- **8 種專案 Profile** — PHP / Python Web / Python AI / Unity / Obsidian / Vue / Flutter / Cocos 各有專屬規範
- **23 個自定義 Commands** — 進度追蹤、Code Review、角色切換、API 管理、PPT 生成等
- **規格說明自動載入** — `SessionStart` hook 自動載入 `.claude/claude_specs/` 下的規範文件
- **多 LLM 配置模板** — 內建阿里雲 Qwen、GLM 等多個 LLM 服務的 settings 範本

---

## 一鍵安裝

```bash
# 1. Clone 本 repo
git clone https://github.com/your-username/ClaudeCodePrf.git

# 2. 執行安裝腳本
cd ClaudeCodePrf

# macOS / Linux
bash setup.sh

# Windows
setup.bat
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
| PHP | `profiler/claude_php.md` | Laravel 11 + Vue 3 + Tailwind，含 RBAC、三端適配 |
| Python Web | `profiler/claude_pyweb.md` | FastAPI / Django，含 SQLAlchemy、Pydantic、pytest |
| Python AI | `profiler/claude_pyai.md` | PyTorch、LLM 應用、電腦視覺，含模型管理、推理服務 |
| Unity | `profiler/claude_unity.md` | Unity 2022.3 LTS，C# 規範、Log 分析、Package 管理 |
| Obsidian | `profiler/claude_obsi.md` | Obsidian Vault 管理、Dataview 查詢、任務篩選 |
| Vue | `profiler/claude_vue.md` | Vue 3 / Nuxt，前端工程開發 |
| Flutter | `profiler/claude_flutter.md` | Flutter / Dart，跨平台應用開發 |
| Cocos | `profiler/claude_cocos.md` | Cocos Creator 遊戲開發 |

---

## Commands 速查表

### 核心 Commands

| 命令 | 說明 |
|------|------|
| `/save` | 保存當前 Session 進度到 `.claude/session.md` |
| `/resume` | 讀取並恢復上次 Session 進度 |
| `/bye` | 執行 `/save` 保存進度後，結束本次 Session |
| `/task` | 將目前項目進度記錄到 task list |
| `/path` | 打印目前工作目錄完整路徑 |
| `/readme` | 更新目前項目的 `README.md` 使用手冊 |
| `/report` | 生成專案狀態報告（進度、問題、建議） |
| `/review` | 對最近修改的文件進行 Code Review |
| `/role {角色}` | 切換到指定角色口吻（如：科學家、產品經理） |
| `/conv {title}` | 將對話重點歸納到 `.claude/conv/conv_{title}.md` |

### 開發工具 Commands

| 命令 | 說明 |
|------|------|
| `/api {init\|ana\|docs}` | API 統一管理：初始化接口、分析差異同步、生成文檔 |
| `/env-check` | 檢查當前開發環境（Python / Node / Git / 依賴）狀態 |
| `/architecture` | 分析專案結構，輸出 Excalidraw 兼容的架構圖 |
| `/export-arch-html` | 將技術架構文檔轉為 HTML 供內部成員瀏覽 |
| `/unicmd` | 驅動 Unity 執行 GmCommand（自然語言 → 指令轉換 → HTTP 橋接） |
| `/wp` | WePages 工單管理 |

### 匯出 Commands

| 命令 | 說明 |
|------|------|
| `/export-math` | 將 Session 中使用的數學模型匯出到 `.claude/math.md` |
| `/load-math` | 載入 `.claude/math.md` 中的數學模型作為上下文 |
| `/export-talk` | 將 `.jsonl` 對話記錄導出為可讀 Markdown |
| `/ppt` | 生成項目簡報 PPT（會先提問確認需求，再生成） |

### Obsidian Commands

| 命令 | 說明 |
|------|------|
| `/obs-pdf` | 將 Obsidian Markdown 檔案轉換為 PDF |
| `/obs-todo` | 篩選並顯示未完成任務 |
| `/obs-plt` | 篩選並顯示已完成任務 |

---

## 舊版升級

如果你的專案還在使用舊版結構（profile 文件在根目錄），可以用 `refhier.bat` 一鍵重整：

1. 複製最新的 `README.md` 和 `refhier.bat` 到你的專案根目錄
2. 執行 `refhier.bat`

腳本會自動：
- 將 `claude_*.md` 從根目錄搬移至 `profiler/`
- 更新 `CLAUDE.md` 中的路徑引用

---

## 手動安裝

如果不使用安裝腳本，可以手動複製文件：

```bash
# 1. 複製基礎配置
cp CLAUDE.md /path/to/your/project/

# 2. 複製 Profile（以 PHP 為例）
mkdir -p /path/to/your/project/profiler
cp profiler/claude_php.md /path/to/your/project/profiler/

# 3. 在 CLAUDE.md 末尾加入載入指令
echo '請同時讀取並遵守 profiler/claude_php.md 中的所有規則。' >> /path/to/your/project/CLAUDE.md

# 4. 建立目錄結構
mkdir -p /path/to/your/project/.claude/commands

# 5. 複製 Commands
cp .claude/commands/*.md /path/to/your/project/.claude/commands/

# 6. 初始化 Session 記錄
cp templates/session.md /path/to/your/project/.claude/session.md

# 7. (可選) 複製規格說明文件
mkdir -p /path/to/your/project/profiler
cp profiler/claude_spc_*.md /path/to/your/project/profiler/
```

---

## 目錄結構

### 本 Repo 結構

```
ClaudeCodePrf/
├── setup.sh                    # 交互式安裝腳本 (macOS/Linux)
├── setup.bat                   # 交互式安裝腳本 (Windows)
├── refhier.bat                 # 舊版目錄結構重整工具
├── CLAUDE.md                   # 全局基礎配置
├── profiler/                   # 專案 Profile 目錄
│   ├── claude_php.md           # PHP Profile
│   ├── claude_pyweb.md         # Python Web Profile
│   ├── claude_pyai.md          # Python AI / LLM / CV Profile
│   ├── claude_unity.md         # Unity Profile
│   ├── claude_obsi.md          # Obsidian Profile
│   ├── claude_vue.md           # Vue Profile
│   ├── claude_flutter.md       # Flutter Profile
│   ├── claude_cocos.md         # Cocos Profile
│   ├── claude_spc_fetchweb.md  # 規格：網站資訊獲取
│   └── claude_spc_unity_log.md # 規格：Unity Log 分析
├── .claude/
│   ├── .env.sample             # 環境變數模板
│   ├── settings.local.json     # MCP / LLM 設定
│   ├── session.md              # Session 進度記錄
│   ├── scripts/                # 自動化腳本
│   │   └── load-specs.sh       # 規格文件自動載入腳本
│   ├── conv/                   # 對話歸檔目錄
│   ├── skills/                 # Skill 定義文件
│   └── commands/               # 23 個自定義命令
│       ├── save.md
│       ├── resume.md
│       ├── bye.md
│       ├── task.md
│       ├── path.md
│       ├── readme.md
│       ├── report.md
│       ├── review.md
│       ├── role.md
│       ├── conv.md
│       ├── api.md
│       ├── env-check.md
│       ├── architecture.md
│       ├── export-arch-html.md
│       ├── unicmd.md
│       ├── wp.md
│       ├── export-math.md
│       ├── load-math.md
│       ├── export-talk.md
│       ├── ppt.md
│       ├── obs-pdf.md
│       ├── obs-todo.md
│       └── obs-plt.md
├── claude-setting/             # 多 LLM 服務 settings 範本
│   ├── settings - aliyun - qwen3.json
│   ├── settings - glm.json
│   └── settings - origin.json
├── src/                        # 工具程式碼
│   └── ai_skill_collector.py   # AI 技能資料收集器
├── unity/                      # Unity 相關文檔
├── cocos/                      # Cocos 相關文檔
└── templates/                  # 安裝用模板文件
    ├── session.md
    └── settings.apify.json
```

### 安裝後的目標專案結構

```
your-project/
├── CLAUDE.md                      # 全局規則
├── profiler/
│   ├── claude_<type>.md           # 專案 Profile
│   └── claude_spc_<topic>.md      # 規格說明文件 (可選)
├── .claude/
│   ├── session.md                 # 進度記錄
│   ├── commands/                  # 自定義命令
│   │   ├── save.md
│   │   └── ...
│   ├── conv/                      # 對話歸檔
│   ├── scripts/                   # 自動化腳本
│   ├── skills/                    # Skill 定義文件 (可選)
│   ├── settings.local.json        # MCP / LLM 配置 (可選)
│   └── .env.sample                # 環境變數模板 (可選)
└── ...
```

---

## .claudeignore 配置

`.claudeignore` 的作用類似 `.gitignore`，用於指定 Claude Code 應忽略的文件和目錄（不會被讀取或索引）。

**重要：`.claudeignore` 必須放在專案根目錄下才會生效。** 放在子目錄中不會被識別。

```
your-project/
├── .claudeignore          # ← 必須在根目錄
├── CLAUDE.md
└── ...
```

範例 `.claudeignore`：

```gitignore
# 模型權重與大型二進制文件
weights/
*.pt
*.onnx
*.bin
*.safetensors

# 數據集
data/raw/
data/processed/

# 編譯產物
node_modules/
__pycache__/
dist/
build/

# 其他
*.log
.env
```

---

## 多 LLM 配置

`claude-setting/` 目錄提供多個 LLM 服務的 settings 範本：

| 配置文件 | 說明 |
|----------|------|
| `settings - origin.json` | 預設原始配置 |
| `settings - aliyun - qwen3.json` | 阿里雲 Qwen3 模型配置 |
| `settings - glm.json` | 智譜 GLM 模型配置 |

使用方式：將對應的 JSON 內容複製或合併到 `.claude/settings.local.json` 中。

---

## 規格說明文件

規格說明文件放置於 `profiler/` 目錄下，命名為 `claude_spc_<topic>.md`，透過 `SessionStart` hook 自動載入。

| 規格文件 | 說明 |
|----------|------|
| `claude_spc_fetchweb.md` | 網站資訊獲取流程與規範 |
| `claude_spc_unity_log.md` | Unity Log 擷取與分析注意事項 |

---

## License

MIT
