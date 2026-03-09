# Export Talk - 導出對話記錄為 Markdown

將 Claude Code 的 `.jsonl` 對話記錄解析為可讀的 Markdown 文件。

## 執行步驟

1. **確認導出範圍**
   - 如用戶指定了特定 session 或 .jsonl 路徑，使用該路徑
   - 否則預設導出當前項目的最新一筆對話記錄
   - `$ARGUMENTS` 可傳入: `list`（列出所有記錄）、`.jsonl 路徑`、或輸出檔名

2. **執行導出腳本**
   - 運行 `python src/export_talk.py` 搭配對應參數
   - 可用參數:
     - `--list` / `-l`: 列出所有可用記錄
     - `--input <path>` / `-i`: 指定 .jsonl 路徑
     - `--output <path>` / `-o`: 指定輸出路徑
     - `--project <keyword>` / `-p`: 項目關鍵字篩選

3. **輸出結果**
   - 預設輸出到 `.claude/conv/talk_<session_id>.md`
   - 告知用戶輸出路徑與訊息統計

## 用法範例

- `/export-talk` — 導出當前項目最新對話
- `/export-talk list` — 列出所有可用對話記錄
- `/export-talk -o docs/meeting_notes.md` — 指定輸出路徑
