# claude_obsi.md — Obsidian 專案配置 Profile

> 本文件為 Obsidian Vault 專案的 Claude Code 補充規則，需搭配 `CLAUDE.md` 主文件使用。
> 放置於專案根目錄，與 CLAUDE.md 同級。

---

## 一、專案基礎資訊

```yaml
# ⚠️ 請根據實際專案填寫以下內容
tool: Obsidian
vault_path: ./                       # Vault 根目錄路徑
default_format: Markdown (.md)
plugins:
  - Dataview                         # 資料查詢
  - Templater                        # 模板引擎
  - Tasks                            # 任務管理
  - Excalidraw                       # 繪圖
language: zh-TW                      # 筆記主要語言
```

---

## 二、Obsidian Vault 結構約定

```
vault-root/
├── 00-Inbox/              # 快速捕獲，未整理的筆記
├── 01-Projects/           # 進行中的專案筆記
├── 02-Areas/              # 持續關注的領域（健康、財務等）
├── 03-Resources/          # 參考資料、學習筆記
├── 04-Archives/           # 已完成或不再活躍的內容
├── Templates/             # Obsidian 模板
├── Attachments/           # 圖片、PDF 等附件
├── Daily/                 # 日記 / Daily Notes
├── .obsidian/             # Obsidian 設定（不應手動修改）
├── CLAUDE.md
└── claude_obsi.md         # ← 本文件
```

---

## 三、Markdown 與 Obsidian 語法規範

### 3.1 連結與引用

- 內部連結使用 Wiki-link 格式：`[[筆記名稱]]` 或 `[[筆記名稱|顯示文字]]`
- 嵌入引用使用：`![[筆記名稱]]` 或 `![[筆記名稱#標題]]`
- 外部連結使用標準 Markdown：`[文字](URL)`
- 圖片統一存放至 `Attachments/`，引用方式：`![[image.png]]`

### 3.2 標籤規範

- 使用 `#tag` 格式，支持巢狀標籤：`#project/web`
- 常用標籤約定：
  - `#status/todo` — 待處理
  - `#status/doing` — 進行中
  - `#status/done` — 已完成
  - `#type/note` — 一般筆記
  - `#type/meeting` — 會議記錄
  - `#type/reference` — 參考資料

### 3.3 Front Matter (YAML)

所有筆記建議包含 front matter：

```yaml
---
title: 筆記標題
date: 2026-02-27
tags:
  - tag1
  - tag2
status: draft | active | done | archived
aliases:
  - 別名
---
```

### 3.4 任務格式

遵循 Obsidian Tasks 插件語法：

```markdown
- [ ] 未完成任務
- [x] 已完成任務
- [ ] 帶日期的任務 📅 2026-03-01
- [ ] 帶優先級的任務 ⏫
- [/] 進行中的任務
- [-] 已取消的任務
```

---

## 四、Dataview 查詢規範

### 4.1 常用查詢模式

```dataview
// 列出所有未完成任務
TASK FROM "" WHERE !completed

// 列出特定標籤的筆記
TABLE date, status FROM #project
SORT date DESC

// 列出最近修改的筆記
TABLE file.mtime AS "修改時間" FROM ""
SORT file.mtime DESC
LIMIT 10
```

### 4.2 查詢規則

- Dataview 查詢塊使用 ` ```dataview ` 標記
- DataviewJS 查詢使用 ` ```dataviewjs ` 標記
- 複雜查詢加上註釋說明用途
- 避免在大量筆記的 vault 中使用過於複雜的 DataviewJS 查詢（影響效能）

---

## 五、模板規範

### 5.1 模板存放

所有模板放在 `Templates/` 目錄下，使用 Templater 語法。

### 5.2 常用模板結構

| 模板名稱 | 用途 | 檔名 |
|----------|------|------|
| 日記模板 | Daily Note | `Templates/daily.md` |
| 會議記錄 | 會議紀要 | `Templates/meeting.md` |
| 專案模板 | 新專案建立 | `Templates/project.md` |
| 讀書筆記 | 書籍/文章摘要 | `Templates/reading.md` |
| 人物筆記 | 人物資訊卡 | `Templates/person.md` |

---

## 六、PDF 轉換系統

### 6.1 轉換規則

當執行 `obs-pdf` 時，按以下流程處理：

1. **讀取** 指定的 Obsidian Markdown 文件
2. **解析** 內容，處理 Obsidian 專屬語法：
   - 將 `[[wikilink]]` 轉為純文字或標準 Markdown 連結
   - 將 `![[embed]]` 展開為嵌入的內容（僅展開一層）
   - 保留圖片引用，轉為標準 `![](path)` 格式
   - 移除 Dataview 查詢塊（無法在 PDF 中執行）
   - 保留 front matter 作為文件資訊頭
3. **轉換** 為 PDF 格式，使用 pandoc 或等效工具
4. **輸出** PDF 文件到同目錄，檔名為 `<原檔名>.pdf`

### 6.2 PDF 樣式

- 頁面大小：A4
- 字體：支持中文顯示（Noto Sans CJK 或系統中文字體）
- 程式碼塊：保留語法高亮
- 標題層級：保留原始層級結構

---

## 七、任務篩選系統

### 7.1 未完成任務篩選（obs-todo）

當執行 `obs-todo` 時：

1. **讀取** 指定的 Obsidian Markdown 文件
2. **掃描** 所有任務項目，篩選出未完成的任務：
   - `- [ ]` — 未開始
   - `- [/]` — 進行中
3. **保留** 任務的上下文資訊：
   - 所屬標題（最近的父級標題）
   - 截止日期（如有 📅 標記）
   - 優先級（如有 ⏫🔼🔽 標記）
4. **輸出** 到 console，格式如下：

```markdown
# 未完成任務 — <檔案名稱>
## 掃描時間: YYYY-MM-DD HH:MM

### ⏫ 高優先級
- [ ] 任務內容 📅 2026-03-01
  └─ 來源章節: ## 第二章

### 🔼 中優先級
- [ ] 任務內容
  └─ 來源章節: ## 開發計畫

### 一般
- [ ] 任務內容
- [/] 進行中的任務
  └─ 來源章節: ## 待辦事項

---
合計: X 個未完成 | X 個進行中
```

### 7.2 已完成任務篩選（obs-plt）

當執行 `obs-plt` 時：

1. **讀取** 指定的 Obsidian Markdown 文件
2. **掃描** 所有任務項目，篩選出已完成的任務：
   - `- [x]` — 已完成
3. **保留** 任務的上下文資訊：
   - 所屬標題
   - 完成日期（如有 ✅ 標記）
4. **輸出** 到 console，格式如下：

```markdown
# 已完成任務 — <檔案名稱>
## 掃描時間: YYYY-MM-DD HH:MM

### 已完成
- [x] 任務內容 ✅ 2026-02-25
  └─ 來源章節: ## 第一階段
- [x] 任務內容
  └─ 來源章節: ## 準備工作

---
合計: X 個已完成
```

---

## 八、指令總覽

| 命令 | 行為 |
|------|------|
| `obs-pdf <docs>` | 將 Obsidian 檔案轉成 PDF 格式 |
| `obs-todo <docs>` | 篩選檔案中未完成的任務，打印到 console |
| `obs-plt <docs>` | 篩選檔案中已完成的任務，打印到 console |

---

## 九、編輯規則

### 9.1 修改筆記時的注意事項

- **不可破壞** 現有的 Wiki-link 連結結構
- **不可移除** front matter 中的既有欄位
- **不可修改** `.obsidian/` 目錄下的任何設定文件
- 新增內容時保持與現有筆記一致的格式風格
- 保留原始的標題層級結構，不隨意提升或降低

### 9.2 批量操作安全規則

- 批量重命名前先列出所有受影響的反向連結
- 移動筆記前確認所有 `[[wikilink]]` 引用已更新
- 刪除筆記前檢查是否有其他筆記引用該筆記

---

## 十、效能建議

- Vault 超過 1000 篇筆記時，避免使用全域 Dataview 查詢
- 圖片建議壓縮後再存入 `Attachments/`
- 定期將不活躍的筆記移入 `04-Archives/`
- 避免單篇筆記超過 10,000 字，考慮拆分為多篇並用連結串接
