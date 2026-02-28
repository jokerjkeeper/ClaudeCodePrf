# Architecture Diagram

分析當前專案結構，輸出 Excalidraw 兼容的 JSON 架構圖。

## 執行步驟

1. 掃描專案目錄結構，識別：
   - 主要模組與服務
   - 資料庫相關文件
   - API 端點
   - 外部服務整合
   - 前端 / 後端分層

2. 分析模組間的依賴與資料流關係：
   - import / require 依賴
   - API 調用關係
   - 資料庫存取路徑
   - 事件或消息傳遞

3. 使用以下節點類型映射生成 Excalidraw JSON：

| 概念 | Excalidraw 圖形 | 顏色 |
|------|-----------------|------|
| 模組 / 服務 | 矩形 (rectangle) | #a5d8ff |
| 資料庫 | 圓柱體 (ellipse) | #ffd8a8 |
| API 端點 | 圓角矩形 (rectangle, roundness) | #b2f2bb |
| 外部服務 | 菱形 (diamond) | #ffec99 |
| 資料流 | 箭頭 (arrow) | #868e96 |
| 使用者 | 橢圓 (ellipse) | #eebefa |

4. 將生成的 JSON 保存到 `.claude/architecture.excalidraw`

5. 輸出架構摘要，包含：
   - 識別到的模組數量
   - 主要的資料流路徑
   - 架構圖的文字描述
   - 告知用戶可用 Excalidraw 開啟 `.claude/architecture.excalidraw` 查看
