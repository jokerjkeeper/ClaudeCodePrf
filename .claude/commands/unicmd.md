---
description: "unicmd — 驅動 Unity 執行 GmCommand（自然語言 → 指令轉換 → HTTP 橋接）"
user_invocable: true
---

# unicmd

透過自然語言驅動 Unity 執行 GmCommand。

## 使用方式

```
/unicmd <自然語言描述>
```

## 範例

```
/unicmd 清除本地成就狀態
/unicmd 列出所有成就
/unicmd 設定 HP 999
/unicmd 切換關卡 5
/unicmd 存檔 1
/unicmd 觸發成就事件 CompltStage 5
```

## 執行流程

1. 讀取 `.claude/skills/unity-driver/SKILL.md` 中的指令對照表
2. 將用戶的自然語言比對為對應的 GmCommand + 參數
3. 透過 `curl -s -X POST http://127.0.0.1:8201/invoke` 發送指令，即時取得執行結果
4. 將 Unity 回傳的 output/error 以易讀格式呈現給用戶

## 注意事項

- Unity 必須正在運行且 CommandBridge 已啟動
- 連線失敗時，提示用戶確認 Unity 是否運行中（可用 `curl http://127.0.0.1:8201/ping` 測試）
- 如果指令需要參數但用戶未提供，應主動詢問
- 對照表未涵蓋的指令，告知用戶該指令不在支援範圍
