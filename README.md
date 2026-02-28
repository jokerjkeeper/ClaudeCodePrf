# 快速上手指南

## 這套模板是什麼？

這是一套 **Claude Code 工作流規範化配置模板**，讓 Claude Code 在不同技術棧的專案中
能自動遵守統一的開發規範、追蹤進度、管理權限。

---

## 文件清單

| 文件 | 用途 |
|------|------|
| `CLAUDE.md` | **全局基礎配置**（必用） — Session 管理、命令定義、權限分級、代碼規範 |
| `claude_unity.md` | Unity 專案 Profile — C# 規範、Log 分析、Package 管理 |
| `claude_php.md` | PHP Web 專案 Profile — Laravel 規範、RBAC、三端適配 |
| `claude_pyweb.md` | Python Web 專案 Profile — FastAPI/Django 規範、RBAC、API 設計 |
| `templates/session.md` | Session 進度記錄模板 |

---

## 使用方式

### 步驟一：複製基礎文件

將 `CLAUDE.md` 複製到你的專案根目錄：

```bash
cp CLAUDE.md /path/to/your/project/CLAUDE.md
```

### 步驟二：選擇並複製 Profile

根據專案類型，複製對應的 profile 文件：

```bash
# Unity 專案
cp claude_unity.md /path/to/your/project/claude_unity.md

# PHP 專案
cp claude_php.md /path/to/your/project/claude_php.md

# Python Web 專案
cp claude_pyweb.md /path/to/your/project/claude_pyweb.md
```

### 步驟三：修改 CLAUDE.md 末尾

在 `CLAUDE.md` 最後加上一行，指定要載入的 profile：

```markdown
請同時讀取並遵守 claude_unity.md 中的所有規則。
```

### 步驟四：初始化 .claude 目錄

```bash
mkdir -p .claude/reports .claude/references .claude/decisions
cp templates/session.md .claude/session.md
```

### 步驟五：自定義配置

打開對應的 profile 文件，修改「專案基礎資訊」區塊中的 yaml 配置，
填入你的實際技術棧版本和選擇。

---

## 目錄結構示例

```
your-project/
├── CLAUDE.md                      # 全局規則
├── claude_php.md                  # 專案 profile（以 PHP 為例）
├── .claude/
│   ├── session.md                 # 進度記錄
│   ├── math.md                    # 數學模型（按需）
│   ├── permissions.log            # 權限操作日誌
│   ├── architecture.excalidraw    # 架構圖（/architecture 生成）
│   ├── references/
│   │   └── buyer.md               # 已購買插件清單（Unity）
│   ├── reports/                   # Log 分析報告（Unity）
│   └── decisions/                 # 架構決策記錄
├── src/
└── ...
```

---

## 常用命令速查

| 命令 | 說明 |
|------|------|
| `/save` | 保存當前進度 |
| `/resume` | 讀取並恢復上次進度 |
| `/architecture` | 生成 Excalidraw 架構圖 |
| `/report` | 生成專案狀態報告 |
| `/review` | Code review 最近修改 |
| `/init-auth` | 生成認證 + 權限系統（PHP / Python） |
| `/make-crud <model>` | 生成完整 CRUD 代碼（PHP / Python） |
| `/analyze-log <path>` | 分析 Unity log（Unity） |
| `/check-security` | 安全掃描（PHP / Python） |
| `/task` | 將目前項目進度記錄到 task |
