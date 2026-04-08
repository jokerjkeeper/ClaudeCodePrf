@echo off
chcp 65001 >nul

REM 支持命令列參數帶入目錄，預設為 J:\爱给网源码
if "%~1"=="" (
    set "TARGET_DIR=J:\爱给网源码"
) else (
    set "TARGET_DIR=%~1"
)

echo MD Docs Viewer 生成中...
echo 掃描目錄: %TARGET_DIR%
python "%~dp0md_viewer.py" "%TARGET_DIR%"
pause
