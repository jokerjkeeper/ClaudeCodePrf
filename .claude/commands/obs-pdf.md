# Obsidian to PDF

將指定的 Obsidian Markdown 檔案轉換為 PDF 格式。

## 參數

- `$ARGUMENTS` — 要轉換的 Obsidian Markdown 檔案路徑

## 執行步驟

1. **讀取檔案**
   - 讀取 `$ARGUMENTS` 指定的 Markdown 檔案
   - 如果檔案不存在，提示錯誤並終止

2. **解析 Obsidian 專屬語法**
   - 將 `[[wikilink]]` 轉為純文字或標準 Markdown 連結
   - 將 `[[wikilink|顯示文字]]` 轉為顯示文字
   - 將 `![[embed]]` 嘗試展開嵌入內容（僅展開一層），找不到來源則保留為文字
   - 將 `![[image.png]]` 轉為標準 `![](Attachments/image.png)` 格式
   - 移除 Dataview 查詢塊（` ```dataview ` / ` ```dataviewjs `），替換為「[Dataview 查詢，僅在 Obsidian 中可用]」
   - 保留 front matter 作為文件資訊頭

3. **轉換為 PDF**
   - 使用 `pandoc` 將處理後的 Markdown 轉為 PDF
   - 如果系統未安裝 pandoc，提示使用者安裝方式並終止
   - pandoc 參數：
     - 頁面大小：A4
     - 中文字體：使用系統可用的 CJK 字體（如 `"Microsoft YaHei"` 或 `"Noto Sans CJK TC"`）
     - PDF 引擎：`xelatex`（支持中文）
   - 輸出路徑：與原檔案同目錄，檔名為 `<原檔名>.pdf`

4. **輸出結果**
   - 顯示轉換成功訊息與 PDF 輸出路徑
   - 如有語法轉換的警告（如找不到嵌入來源），一併列出
