# Code Review

對最近修改的文件進行全面的 code review。

## 執行步驟

1. **取得變更範圍**
   - 取得未提交的變更文件：`git diff --name-only`
   - 取得已暫存的變更文件：`git diff --cached --name-only`
   - 如果沒有未提交變更，取得最近一次 commit 的變更：`git diff HEAD~1 --name-only`

2. **逐一審查每個變更文件**，檢查以下項目：

### 安全問題 (CRITICAL)
- 是否有 hardcoded 的密鑰、API key、token、密碼
- SQL injection 風險
- XSS 漏洞
- 缺少輸入驗證
- 不安全的依賴使用
- 路徑遍歷風險

### 代碼質量 (HIGH)
- 函數是否超過 50 行
- 文件是否超過 800 行
- 巢狀層級是否超過 4 層
- 是否缺少錯誤處理
- 是否有殘留的 console.log / print 調試語句
- 是否有未處理的 TODO / FIXME

### 最佳實踐 (MEDIUM)
- 命名是否清晰有意義
- 是否有重複代碼可以抽取
- 是否缺少對新增代碼的測試
- 是否符合專案現有的代碼風格

3. **生成審查報告**

對每個發現的問題，提供：
- **嚴重等級**: CRITICAL / HIGH / MEDIUM / LOW
- **文件位置**: 文件路徑與行號
- **問題描述**: 具體說明問題
- **修復建議**: 提供具體的修復方式

4. **總結**
   - 審查文件總數
   - 各等級問題數量統計
   - 是否建議通過（無 CRITICAL 或 HIGH 問題時建議通過）
   - 如果有 CRITICAL 或 HIGH 問題，明確指出必須修復後才能提交
