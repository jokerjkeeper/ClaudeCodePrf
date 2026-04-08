# Docs Viewer — 生成 Markdown 文檔瀏覽器

執行 Python 腳本掃描當前項目所有 `.md` 檔案，生成自包含的 `docs-viewer.html`。

## 執行步驟

1. 執行以下命令：
   ```bash
   python src/md_viewer.py --dir . --output docs-viewer.html
   ```
2. 告知用戶生成結果（檔案數量、輸出路徑）
3. 提示用戶可直接用瀏覽器開啟 `docs-viewer.html`

## 注意事項

- 每次執行會重新掃描並覆蓋舊的 `docs-viewer.html`
- 新增或修改 `.md` 檔案後重跑此命令即可刷新
- 排除目錄：`.git`、`node_modules`、`__pycache__`、`.venv` 等
- 快捷鍵：`Ctrl+K` 聚焦搜尋框、`Esc` 清除搜尋
