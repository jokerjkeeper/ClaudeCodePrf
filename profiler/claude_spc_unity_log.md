# Unity Log 分析流程

> 本規格適用於所有 Unity Editor.log 及 Player.log 的分析任務。

---

## 注意事項

**禁止直接讀取完整 Editor.log。**

Unity 的 log 檔案通常非常大（數萬至數十萬行），直接讀取會導致 context 爆量，嚴重影響分析品質。

---

## 擷取命令

分析前必須先使用以下命令擷取片段：

| 用途 | 命令 |
|------|------|
| 最近錯誤 | `grep -n "ERROR\|Exception" [LOG_PATH] \| tail -20` |
| 最近 200 行 | `tail -n 200 [LOG_PATH]` |
| 特定關鍵字 | `grep -n "[KEYWORD]" [LOG_PATH] \| tail -30` |
| 帶上下文的錯誤 | `grep -n -A 5 "ERROR\|Exception" [LOG_PATH] \| tail -50` |

> `[LOG_PATH]` 請替換為實際 log 路徑，參考 `profiler/claude_unity.md` 3.1 節的平台路徑對照表。

---

## 分析流程

1. **擷取** — 使用上述命令取得 log 片段（禁止直接讀取完整檔案）
2. **分類** — 將日誌條目分類為 ERROR / WARNING / EXCEPTION
3. **去重** — 相同錯誤訊息合併，統計出現次數
4. **報告** — 按 `profiler/claude_unity.md` 3.3 節格式生成報告
