## 網站資訊獲取規則

當需要獲取網站資訊時，按以下順序判斷：

### 模式 1：Raw Fetch（預設）
- 先用 curl 或 fetch 取得原始 HTML
- 適用條件：靜態網站、只需要 HTML/CSS/JS 原始碼、技術分析
- 判斷標準：如果取回的 HTML body 內容充實，就用這個結果

### 模式 2：Rendered Fetch（回退）
- 當模式 1 結果不完整時自動切換
- 觸發條件：
  - HTML body 很小（< 1KB 有效內容）
  - 發現 React/Vue/Angular/Next.js 等 SPA 框架標記
  - 頁面主要內容在 <noscript> 提示中
  - 用戶明確要求「看到的頁面內容」
- 使用 Apify website-content-crawler Actor

### 模式 3：結構化資料獲取
- 當目標是特定平台時直接使用
- 觸發條件：URL 屬於 Instagram、YouTube、Google Maps、
  TikTok、Facebook、Booking.com、TripAdvisor 等
- 使用 apify-ultimate-scraper skill 自動選擇對應 Actor