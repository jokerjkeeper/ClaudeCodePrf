# Apify Ultimate Scraper Skill

## 用途

使用 Apify 的 Universal Scraper 爬取指定網頁內容，支持靜態與動態頁面。

## 使用方式

當用戶需要爬取網頁資料時，使用 Apify MCP Server 調用 scraper actor。

## 典型場景

- 爬取網頁文章內容並整理為 Markdown
- 批量提取結構化資料（表格、列表、價格等）
- 抓取動態渲染的 SPA 頁面內容
- 監控網頁變化

## 調用範例

```
使用 Apify 爬取 <URL> 的內容，提取以下資訊：
- 標題
- 正文內容
- 所有連結
```

## 注意事項

- 需要有效的 `APIFY_TOKEN` 環境變數
- 遵守目標網站的 robots.txt 規則
- 爬取頻率應合理，避免對目標站點造成負擔
- 敏感資料不應存儲在版本控制中
