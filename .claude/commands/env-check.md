# Env Check — 開發環境檢查

檢查當前開發環境狀態，確保在正確的環境中工作。

## 執行步驟

1. **Python 環境檢查**
   - 執行 `conda info --envs` 列出所有 conda 環境，標記當前啟用的環境
   - 執行 `python --version` 確認 Python 版本
   - 執行 `pip --version` 確認 pip 來源路徑（確認是否指向正確環境）
   - 若未啟用任何 conda 環境（在 base 中），**警告用戶**可能需要先切換環境

2. **Node.js 環境檢查**
   - 執行 `node -v` 確認 Node 版本
   - 執行 `npm -v` 確認 npm 版本
   - 檢查是否存在 `package.json`，若存在確認 `node_modules/` 是否已安裝

3. **項目環境檢查**
   - 檢查是否存在 `.env` 文件
   - 檢查是否存在 `requirements.txt` / `pyproject.toml` / `composer.json` / `pubspec.yaml` 等依賴定義文件
   - 若存在依賴文件但未安裝依賴，提醒用戶

4. **Git 環境檢查**
   - 執行 `git branch --show-current` 顯示當前分支
   - 若在 `main` / `master` 分支上，**提醒用戶**應切換到功能分支再開發

5. **輸出摘要**
   - 以表格形式呈現所有檢查結果：

   | 項目 | 狀態 | 值 |
   |------|------|-----|
   | Python 版本 | ✅ / ⚠️ | 3.x.x |
   | Conda 環境 | ✅ / ⚠️ | env_name |
   | Node 版本 | ✅ / ❌ | v2x.x.x |
   | Git 分支 | ✅ / ⚠️ | feature/xxx |
   | 依賴安裝 | ✅ / ⚠️ | 已安裝 / 未安裝 |

   - ✅ = 正常
   - ⚠️ = 需注意（不阻塞但建議處理）
   - ❌ = 未安裝或不可用
