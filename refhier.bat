@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

:: ============================================================================
:: refhier.bat — 目錄結構重整工具
:: 將舊版 ClaudeCodePrf 的 profile 文件從根目錄搬移至 profiler/ 目錄
:: 並自動更新 CLAUDE.md 中的路徑引用
:: ============================================================================

:: --- 取得腳本所在目錄 ---
set "WORK_DIR=%~dp0"
if "%WORK_DIR:~-1%"=="\" set "WORK_DIR=%WORK_DIR:~0,-1%"

:: --- Profile 清單 ---
set "PROFILES=claude_php.md claude_pyweb.md claude_unity.md claude_obsi.md"
set "MOVED=0"
set "SKIPPED=0"

:: ============================================================================
:: 歡迎畫面
:: ============================================================================
cls
echo.
echo    ╔══════════════════════════════════════════╗
echo    ║                                          ║
echo    ║     ClaudeCodePrf  Restructure  Tool     ║
echo    ║                                          ║
echo    ║      目錄結構重整 — 遷移至新版結構       ║
echo    ║                                          ║
echo    ╚══════════════════════════════════════════╝
echo.
echo    工作目錄: %WORK_DIR%
echo.
echo    本工具會將根目錄的 profile 文件搬移至 profiler\ 目錄，
echo    並更新 CLAUDE.md 中的路徑引用。
echo.

:: ============================================================================
:: 檢查是否有需要搬移的文件
:: ============================================================================
set "HAS_FILES=0"
for %%f in (%PROFILES%) do (
    if exist "%WORK_DIR%\%%f" set "HAS_FILES=1"
)

if "%HAS_FILES%"=="0" (
    echo   [i] 未偵測到根目錄中的 profile 文件。
    echo.
    if exist "%WORK_DIR%\profiler" (
        echo   [OK] profiler\ 目錄已存在，看起來已是新版結構。
    ) else (
        echo   [!] 既沒有根目錄的 profile 文件，也沒有 profiler\ 目錄。
        echo       請確認是否在正確的專案目錄下執行。
    )
    echo.
    goto :end
)

:: ============================================================================
:: 顯示偵測結果
:: ============================================================================
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   偵測到以下 profile 文件 (將搬移至 profiler\)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

for %%f in (%PROFILES%) do (
    if exist "%WORK_DIR%\%%f" (
        echo     %%f  →  profiler\%%f
    )
)
echo.

:: ============================================================================
:: 確認執行
:: ============================================================================
set "CONFIRM="
set /p "CONFIRM=  確認開始重整? [Y/n] "
if /i "%CONFIRM%"=="n" (
    echo.
    echo   [X] 操作已取消。
    goto :end
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   執行中...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

:: ============================================================================
:: 1) 建立 profiler 目錄
:: ============================================================================
if not exist "%WORK_DIR%\profiler" (
    mkdir "%WORK_DIR%\profiler"
    echo   [OK] 已建立 profiler\ 目錄
) else (
    echo   [i] profiler\ 目錄已存在
)

:: ============================================================================
:: 2) 搬移 profile 文件
:: ============================================================================
echo.
echo   [*] 搬移 profile 文件

for %%f in (%PROFILES%) do (
    if exist "%WORK_DIR%\%%f" (
        if exist "%WORK_DIR%\profiler\%%f" (
            echo   [!] profiler\%%f 已存在，跳過搬移 (原檔保留)
            set /a "SKIPPED+=1"
        ) else (
            move "%WORK_DIR%\%%f" "%WORK_DIR%\profiler\%%f" >nul 2>&1
            if errorlevel 1 (
                echo   [X] 搬移失敗: %%f
                set /a "SKIPPED+=1"
            ) else (
                echo   [OK] %%f  →  profiler\%%f
                set /a "MOVED+=1"
            )
        )
    )
)

:: ============================================================================
:: 3) 更新 CLAUDE.md 中的路徑引用
:: ============================================================================
echo.
echo   [*] 更新 CLAUDE.md 路徑引用

if exist "%WORK_DIR%\CLAUDE.md" (
    set "UPDATED=0"

    :: 建立暫存檔
    set "TMPFILE=%WORK_DIR%\CLAUDE.md.tmp"

    :: 逐行處理，替換路徑引用
    (
        for /f "usebackq delims=" %%L in ("%WORK_DIR%\CLAUDE.md") do (
            set "LINE=%%L"

            :: 替換各種可能的引用格式
            set "LINE=!LINE:請同時讀取並遵守 claude_php.md=請同時讀取並遵守 profiler/claude_php.md!"
            set "LINE=!LINE:請同時讀取並遵守 claude_pyweb.md=請同時讀取並遵守 profiler/claude_pyweb.md!"
            set "LINE=!LINE:請同時讀取並遵守 claude_unity.md=請同時讀取並遵守 profiler/claude_unity.md!"
            set "LINE=!LINE:請同時讀取並遵守 claude_obsi.md=請同時讀取並遵守 profiler/claude_obsi.md!"

            echo(!LINE!
        )
    ) > "!TMPFILE!"

    :: 比較是否有變更
    fc "%WORK_DIR%\CLAUDE.md" "!TMPFILE!" >nul 2>&1
    if errorlevel 1 (
        move /y "!TMPFILE!" "%WORK_DIR%\CLAUDE.md" >nul 2>&1
        echo   [OK] CLAUDE.md 中的 profile 路徑已更新為 profiler\ 前綴
    ) else (
        del "!TMPFILE!" >nul 2>&1
        echo   [i] CLAUDE.md 中未發現需要更新的路徑引用
    )
) else (
    echo   [!] 未找到 CLAUDE.md，跳過路徑更新
)

:: ============================================================================
:: 4) 完成摘要
:: ============================================================================
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   重整完成!
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo   搬移: !MOVED! 個文件
if !SKIPPED! gtr 0 (
    echo   跳過: !SKIPPED! 個文件
)
echo.
echo   新版目錄結構:
echo.
echo     專案根目錄\
echo     ├── CLAUDE.md
echo     ├── profiler\
if exist "%WORK_DIR%\profiler\claude_php.md"    echo     │   ├── claude_php.md
if exist "%WORK_DIR%\profiler\claude_pyweb.md"  echo     │   ├── claude_pyweb.md
if exist "%WORK_DIR%\profiler\claude_unity.md"  echo     │   ├── claude_unity.md
if exist "%WORK_DIR%\profiler\claude_obsi.md"   echo     │   └── claude_obsi.md
echo     ├── .claude\
echo     │   └── commands\
echo     └── ...
echo.

:end
endlocal
pause
