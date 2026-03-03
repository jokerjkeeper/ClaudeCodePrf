@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

:: ============================================================================
:: ClaudeCodePrf — Interactive Setup Script (Windows)
:: 將 Claude Code 工作流配置安裝到目標專案
:: ============================================================================

:: --- 取得腳本所在目錄 ---
set "SCRIPT_DIR=%~dp0"
:: 移除末尾反斜線
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: --- 變數初始化 ---
set "PROFILE_FILE="
set "PROFILE_NAME="
set "ENABLE_APIFY=false"
set "CMD_COUNT=0"

:: ============================================================================
:: 1) 歡迎畫面
:: ============================================================================
cls
echo.
echo    ╔══════════════════════════════════════════╗
echo    ║                                          ║
echo    ║        ClaudeCodePrf  Setup  Tool        ║
echo    ║                                          ║
echo    ║   Claude Code 工作流配置 — 交互式安裝    ║
echo    ║                                          ║
echo    ╚══════════════════════════════════════════╝
echo.
echo    本腳本會將 Claude Code 配置文件安裝到你的專案中。
echo    已存在的文件不會被自動覆蓋。
echo.

:: ============================================================================
:: 2) 詢問目標專案路徑
:: ============================================================================
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   步驟 1/5 — 目標專案路徑
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

:: 預設為腳本所在目錄（當前目錄）
set "DEFAULT_TARGET=%SCRIPT_DIR%"
echo   預設路徑: %DEFAULT_TARGET%
set "TARGET_DIR="
set /p "TARGET_DIR=  請輸入目標專案路徑 (Enter 使用預設): "

if "%TARGET_DIR%"=="" set "TARGET_DIR=%DEFAULT_TARGET%"

:: 驗證路徑
if not exist "%TARGET_DIR%" (
    echo   [!] 路徑不存在: %TARGET_DIR%
    set "CREATE_DIR="
    set /p "CREATE_DIR=  是否建立此目錄? [y/N] "
    if /i "!CREATE_DIR!"=="y" (
        mkdir "%TARGET_DIR%"
        echo   [OK] 已建立目錄: %TARGET_DIR%
    ) else (
        echo   [X] 安裝取消。
        goto :end
    )
)

echo.
echo   [OK] 目標路徑: %TARGET_DIR%
echo.

:: ============================================================================
:: 3) 選擇專案類型 (Profile)
:: ============================================================================
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   步驟 2/5 — 選擇專案類型
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   [1] PHP (Laravel)
echo   [2] Python Web (FastAPI / Django)
echo   [3] Unity (C#)
echo   [4] Obsidian
echo   [0] 不設定 Profile (只安裝基礎 CLAUDE.md)
echo.
set "PROFILE_CHOICE="
set /p "PROFILE_CHOICE=  請選擇 [0-4]: "

if "%PROFILE_CHOICE%"=="1" (
    set "PROFILE_FILE=claude_php.md"
    set "PROFILE_NAME=PHP (Laravel)"
) else if "%PROFILE_CHOICE%"=="2" (
    set "PROFILE_FILE=claude_pyweb.md"
    set "PROFILE_NAME=Python Web"
) else if "%PROFILE_CHOICE%"=="3" (
    set "PROFILE_FILE=claude_unity.md"
    set "PROFILE_NAME=Unity (C#)"
) else if "%PROFILE_CHOICE%"=="4" (
    set "PROFILE_FILE=claude_obsi.md"
    set "PROFILE_NAME=Obsidian"
) else (
    set "PROFILE_FILE="
    set "PROFILE_NAME=無 (僅基礎配置)"
)

echo.
echo   [OK] 專案類型: !PROFILE_NAME!
echo.

:: ============================================================================
:: 4) 選擇 Commands
:: ============================================================================
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   步驟 3/5 — 選擇 Commands
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   [A] 全部啟用 (13 個 commands)
echo   [C] 僅核心 (save, resume, task, path, report, review, role)
echo   [S] 自選模式
echo.
set "CMD_CHOICE="
set /p "CMD_CHOICE=  請選擇 [A/C/S]: "

:: 初始化所有 command flags
for %%c in (save resume task path report review role architecture export-math load-math obs-pdf obs-todo obs-plt) do (
    set "CMD_%%c=0"
)

if /i "%CMD_CHOICE%"=="S" goto :custom_select
if /i "%CMD_CHOICE%"=="C" goto :core_only

:: 預設 A — 全部啟用
:all_cmds
for %%c in (save resume task path report review role architecture export-math load-math obs-pdf obs-todo obs-plt) do (
    set "CMD_%%c=1"
)
set "CMD_COUNT=13"
echo.
echo   [OK] 將安裝全部 13 個 commands
goto :cmd_done

:core_only
for %%c in (save resume task path report review role) do (
    set "CMD_%%c=1"
)
set "CMD_COUNT=7"
echo.
echo   [OK] 將安裝 7 個核心 commands
goto :cmd_done

:custom_select
set "CMD_COUNT=0"
echo.
echo   --- 核心 Commands ---

for %%c in (save resume task path report review role) do (
    set "YN="
    set /p "YN=    啟用 %%c? [Y/n] "
    if /i "!YN!"=="n" (
        set "CMD_%%c=0"
    ) else (
        set "CMD_%%c=1"
        set /a "CMD_COUNT+=1"
    )
)

echo.
echo   --- 進階 Commands ---

for %%c in (architecture export-math load-math) do (
    set "YN="
    set /p "YN=    啟用 %%c? [Y/n] "
    if /i "!YN!"=="n" (
        set "CMD_%%c=0"
    ) else (
        set "CMD_%%c=1"
        set /a "CMD_COUNT+=1"
    )
)

echo.
echo   --- Obsidian Commands ---

for %%c in (obs-pdf obs-todo obs-plt) do (
    set "YN="
    set /p "YN=    啟用 %%c? [y/N] "
    if /i "!YN!"=="y" (
        set "CMD_%%c=1"
        set /a "CMD_COUNT+=1"
    ) else (
        set "CMD_%%c=0"
    )
)

echo.
echo   [OK] 將安裝 !CMD_COUNT! 個 commands

:cmd_done
echo.

:: ============================================================================
:: 5) Apify Skill
:: ============================================================================
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   步驟 4/5 — Apify 網頁爬蟲功能
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   Apify 提供強大的網頁爬蟲 / Scraper 功能。
echo   啟用後將安裝 MCP Server 配置與 Skill 文件。
echo   (需要 Apify API Token，可稍後設定)
echo.
set "APIFY_CHOICE="
set /p "APIFY_CHOICE=  是否啟用 Apify Skill? [y/N] "

if /i "%APIFY_CHOICE%"=="y" (
    set "ENABLE_APIFY=true"
    echo.
    echo   [OK] 將安裝 Apify 配置
) else (
    set "ENABLE_APIFY=false"
    echo.
    echo   [OK] 跳過 Apify
)
echo.

:: ============================================================================
:: 確認安裝
:: ============================================================================
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   步驟 5/5 — 確認安裝
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   目標路徑:   %TARGET_DIR%
echo   專案類型:   !PROFILE_NAME!
echo   Commands:   !CMD_COUNT! 個
if "!ENABLE_APIFY!"=="true" (
    echo   Apify:      啟用
) else (
    echo   Apify:      未啟用
)
echo.
set "CONFIRM="
set /p "CONFIRM=  確認開始安裝? [Y/n] "

if /i "%CONFIRM%"=="n" (
    echo   [X] 安裝已取消。
    goto :end
)

:: ============================================================================
:: 6) 執行安裝
:: ============================================================================
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   安裝中...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

:: --- 建立目錄結構 ---
echo.
echo   [*] 建立目錄結構

if not exist "%TARGET_DIR%\.claude\commands" mkdir "%TARGET_DIR%\.claude\commands"
echo   [OK] .claude\commands\

if "!ENABLE_APIFY!"=="true" (
    if not exist "%TARGET_DIR%\.claude\skills" mkdir "%TARGET_DIR%\.claude\skills"
    echo   [OK] .claude\skills\
)

:: --- 複製 CLAUDE.md ---
echo.
echo   [*] 安裝 CLAUDE.md
call :safe_copy "%SCRIPT_DIR%\CLAUDE.md" "%TARGET_DIR%\CLAUDE.md"

:: --- 複製 Profile ---
if not "!PROFILE_FILE!"=="" (
    echo.
    echo   [*] 安裝 Profile: !PROFILE_NAME!
    call :safe_copy "%SCRIPT_DIR%\!PROFILE_FILE!" "%TARGET_DIR%\!PROFILE_FILE!"

    :: 在 CLAUDE.md 末尾加上 profile 載入指令
    set "LOAD_LINE=請同時讀取並遵守 !PROFILE_FILE! 中的所有規則。"
    findstr /c:"!LOAD_LINE!" "%TARGET_DIR%\CLAUDE.md" >nul 2>&1
    if errorlevel 1 (
        echo.>> "%TARGET_DIR%\CLAUDE.md"
        echo !LOAD_LINE!>> "%TARGET_DIR%\CLAUDE.md"
        echo   [OK] 已在 CLAUDE.md 末尾加入 Profile 載入指令
    ) else (
        echo   [i] CLAUDE.md 中已包含 Profile 載入指令，跳過
    )
)

:: --- 複製 Commands ---
echo.
echo   [*] 安裝 Commands (!CMD_COUNT! 個)

for %%c in (save resume task path report review role architecture export-math load-math obs-pdf obs-todo obs-plt) do (
    if "!CMD_%%c!"=="1" (
        if exist "%SCRIPT_DIR%\.claude\commands\%%c.md" (
            call :safe_copy "%SCRIPT_DIR%\.claude\commands\%%c.md" "%TARGET_DIR%\.claude\commands\%%c.md"
        ) else (
            echo   [!] 找不到 command 文件: %%c.md
        )
    )
)

:: --- 建立 session.md ---
echo.
echo   [*] 初始化 Session 記錄

if exist "%SCRIPT_DIR%\templates\session.md" (
    call :safe_copy "%SCRIPT_DIR%\templates\session.md" "%TARGET_DIR%\.claude\session.md"
) else (
    if not exist "%TARGET_DIR%\.claude\session.md" (
        (
            echo # Session 進度記錄
            echo.
            echo ## 狀態: 尚未開始
            echo ## 最後更新: -
            echo ## 當前分支: main
            echo.
            echo ---
            echo.
            echo ### 當前任務
            echo - （尚未開始）
            echo.
            echo ### 已完成
            echo - （無）
            echo.
            echo ### 待辦
            echo - [ ] 初始化專案
            echo.
            echo ### 決策記錄
            echo.
            echo ^| 日期 ^| 決策 ^| 原因 ^| 替代方案 ^|
            echo ^|------^|------^|------^|----------^|
            echo ^|      ^|      ^|      ^|          ^|
            echo.
            echo ### 已知問題
            echo - （無）
        ) > "%TARGET_DIR%\.claude\session.md"
        echo   [OK] session.md (內建模板)
    ) else (
        echo   [i] session.md 已存在，跳過
    )
)

:: --- Apify 配置 ---
if "!ENABLE_APIFY!"=="true" (
    echo.
    echo   [*] 安裝 Apify 配置

    if exist "%SCRIPT_DIR%\apify-skills\apify-ultimate-scraper.md" (
        call :safe_copy "%SCRIPT_DIR%\apify-skills\apify-ultimate-scraper.md" "%TARGET_DIR%\.claude\skills\apify-ultimate-scraper.md"
    )

    if exist "%SCRIPT_DIR%\.claude\.env.sample" (
        call :safe_copy "%SCRIPT_DIR%\.claude\.env.sample" "%TARGET_DIR%\.claude\.env.sample"
    )

    if exist "%SCRIPT_DIR%\templates\settings.apify.json" (
        call :safe_copy "%SCRIPT_DIR%\templates\settings.apify.json" "%TARGET_DIR%\.claude\settings.local.json"
    )

    echo   [i] 請在 .claude\.env.sample 中填入你的 APIFY_TOKEN
)

:: ============================================================================
:: 7) 安裝摘要
:: ============================================================================
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   安裝完成!
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo   已安裝到: %TARGET_DIR%
echo.
echo   已安裝的文件:
echo     CLAUDE.md                        — 全局基礎配置

if not "!PROFILE_FILE!"=="" (
    echo     !PROFILE_FILE!                   — !PROFILE_NAME! Profile
)

echo     .claude\session.md               — Session 進度記錄
echo     .claude\commands\ (!CMD_COUNT! 個^)         — 自定義命令

if "!ENABLE_APIFY!"=="true" (
    echo     .claude\skills\                  — Apify Skill
    echo     .claude\settings.local.json      — MCP Server 配置
    echo     .claude\.env.sample              — 環境變數模板
)

echo.
echo   下一步:
echo     1. cd %TARGET_DIR%
echo     2. 啟動 Claude Code 開始使用

if not "!PROFILE_FILE!"=="" (
    echo     3. 修改 !PROFILE_FILE! 中的「專案基礎資訊」
)

if "!ENABLE_APIFY!"=="true" (
    echo     4. 在 .claude\.env.sample 中填入 APIFY_TOKEN
)

echo.
echo   感謝使用 ClaudeCodePrf!
echo.
goto :end

:: ============================================================================
:: 工具函數: safe_copy — 若目標已存在則詢問是否覆蓋
:: ============================================================================
:safe_copy
set "SRC=%~f1"
set "DST=%~f2"

:: 來源與目標是同一個檔案時直接跳過
if "%SRC%"=="%DST%" (
    echo   [i] 跳過 (同一檔案^): %~nx2
    goto :eof
)

if exist "%DST%" (
    set "OVERWRITE="
    set /p "OVERWRITE=  [!] 文件已存在: %~nx2 — 是否覆蓋? [y/N] "
    if /i not "!OVERWRITE!"=="y" (
        echo   [i] 跳過: %~nx2
        goto :eof
    )
)

copy /y "%SRC%" "%DST%" >nul 2>&1
if errorlevel 1 (
    echo   [X] 複製失敗: %~nx2
) else (
    echo   [OK] %~nx2
)
goto :eof

:: ============================================================================
:end
endlocal
pause
