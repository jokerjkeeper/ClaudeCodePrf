# Bye — 結束 Session

執行 `/save` 保存當前進度後，結束本次 session。

## 執行步驟

1. 先執行 `/save` 指令，將當前 session 進度寫入 `.claude/session.md`
2. 保存完成後，向用戶告別並提示進度已儲存
3. 結束本次 session（不再接受新的指令）
