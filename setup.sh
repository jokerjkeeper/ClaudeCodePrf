#!/usr/bin/env bash
# ============================================================================
# ClaudeCodePrf — Interactive Setup Script
# 將 Claude Code 工作流配置安裝到目標專案
# ============================================================================

set -euo pipefail

# --- 色碼定義 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

# --- 取得腳本所在目錄（即本 repo 路徑） ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- 工具函數 ---
print_header() {
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}  $1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_step() {
    echo -e "\n${BLUE}▸${NC} ${BOLD}$1${NC}"
}

print_success() {
    echo -e "  ${GREEN}✔${NC} $1"
}

print_warning() {
    echo -e "  ${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "  ${RED}✘${NC} $1"
}

print_info() {
    echo -e "  ${DIM}$1${NC}"
}

# 安全複製：若目標已存在則詢問是否覆蓋
safe_copy() {
    local src="$1"
    local dst="$2"

    # 來源與目標是同一個檔案時直接跳過
    local real_src real_dst
    real_src="$(realpath "$src" 2>/dev/null || echo "$src")"
    real_dst="$(realpath "$dst" 2>/dev/null || echo "$dst")"
    if [[ "$real_src" == "$real_dst" ]]; then
        print_info "跳過 (同一檔案): $(basename "$dst")"
        return 0
    fi

    if [[ -f "$dst" ]]; then
        echo -e -n "  ${YELLOW}⚠${NC} 文件已存在: ${DIM}$(basename "$dst")${NC} — 是否覆蓋? [y/N] "
        read -r overwrite
        if [[ "$overwrite" != "y" && "$overwrite" != "Y" ]]; then
            print_info "跳過: $(basename "$dst")"
            return 0
        fi
    fi

    cp "$src" "$dst"
    print_success "$(basename "$dst")"
}

# ============================================================================
# 1) 歡迎畫面
# ============================================================================
clear 2>/dev/null || true
echo ""
echo -e "${CYAN}"
echo "   ╔══════════════════════════════════════════╗"
echo "   ║                                          ║"
echo "   ║        ClaudeCodePrf  Setup  Tool        ║"
echo "   ║                                          ║"
echo "   ║   Claude Code 工作流配置 — 交互式安裝    ║"
echo "   ║                                          ║"
echo "   ╚══════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "${DIM}   本腳本會將 Claude Code 配置文件安裝到你的專案中。${NC}"
echo -e "${DIM}   已存在的文件不會被自動覆蓋。${NC}"
echo ""

# ============================================================================
# 2) 詢問目標專案路徑
# ============================================================================
print_header "步驟 1/5 — 目標專案路徑"

DEFAULT_TARGET="$SCRIPT_DIR"
echo -e "  預設路徑: ${DIM}$DEFAULT_TARGET${NC}"
echo -n -e "  請輸入目標專案路徑 ${DIM}(Enter 使用預設)${NC}: "
read -r TARGET_DIR

if [[ -z "$TARGET_DIR" ]]; then
    TARGET_DIR="$DEFAULT_TARGET"
fi

# 展開 ~ 為 $HOME
TARGET_DIR="${TARGET_DIR/#\~/$HOME}"

# 驗證路徑
if [[ ! -d "$TARGET_DIR" ]]; then
    print_error "路徑不存在: $TARGET_DIR"
    echo -n -e "  是否建立此目錄? [y/N] "
    read -r create_dir
    if [[ "$create_dir" == "y" || "$create_dir" == "Y" ]]; then
        mkdir -p "$TARGET_DIR"
        print_success "已建立目錄: $TARGET_DIR"
    else
        print_error "安裝取消。"
        exit 1
    fi
fi

echo -e "\n  ${GREEN}✔${NC} 目標路徑: ${BOLD}$TARGET_DIR${NC}"

# ============================================================================
# 3) 選擇專案類型 (Profile)
# ============================================================================
print_header "步驟 2/5 — 選擇專案類型"

echo "  [1] PHP (Laravel)"
echo "  [2] Python Web (FastAPI / Django)"
echo "  [3] Unity (C#)"
echo "  [4] Obsidian"
echo -e "  [0] 不設定 Profile ${DIM}(只安裝基礎 CLAUDE.md)${NC}"
echo ""
echo -n "  請選擇 [0-4]: "
read -r PROFILE_CHOICE

PROFILE_FILE=""
PROFILE_NAME=""

case "$PROFILE_CHOICE" in
    1)
        PROFILE_FILE="claude_php.md"
        PROFILE_NAME="PHP (Laravel)"
        ;;
    2)
        PROFILE_FILE="claude_pyweb.md"
        PROFILE_NAME="Python Web"
        ;;
    3)
        PROFILE_FILE="claude_unity.md"
        PROFILE_NAME="Unity (C#)"
        ;;
    4)
        PROFILE_FILE="claude_obsi.md"
        PROFILE_NAME="Obsidian"
        ;;
    0|"")
        PROFILE_FILE=""
        PROFILE_NAME="無 (僅基礎配置)"
        ;;
    *)
        print_error "無效選擇，將不安裝 Profile。"
        PROFILE_FILE=""
        PROFILE_NAME="無 (僅基礎配置)"
        ;;
esac

echo -e "\n  ${GREEN}✔${NC} 專案類型: ${BOLD}$PROFILE_NAME${NC}"

# ============================================================================
# 4) 選擇 Commands
# ============================================================================
print_header "步驟 3/5 — 選擇 Commands"

# 定義 command 分類
CORE_CMDS=("save" "resume" "task" "path" "report" "review" "role")
ADV_CMDS=("architecture" "export-math" "load-math")
OBSI_CMDS=("obs-pdf" "obs-todo" "obs-plt")

echo "  [A] 全部啟用 (13 個 commands)"
echo "  [C] 僅核心 (save, resume, task, path, report, review, role)"
echo "  [S] 自選模式"
echo ""
echo -n "  請選擇 [A/C/S]: "
read -r CMD_CHOICE

SELECTED_CMDS=()

case "$CMD_CHOICE" in
    A|a|"")
        SELECTED_CMDS=("${CORE_CMDS[@]}" "${ADV_CMDS[@]}" "${OBSI_CMDS[@]}")
        echo -e "\n  ${GREEN}✔${NC} 將安裝全部 13 個 commands"
        ;;
    C|c)
        SELECTED_CMDS=("${CORE_CMDS[@]}")
        echo -e "\n  ${GREEN}✔${NC} 將安裝 7 個核心 commands"
        ;;
    S|s)
        echo ""
        echo -e "  ${BOLD}核心 Commands:${NC}"
        for cmd in "${CORE_CMDS[@]}"; do
            echo -n -e "    啟用 ${CYAN}$cmd${NC}? [Y/n] "
            read -r yn
            if [[ "$yn" != "n" && "$yn" != "N" ]]; then
                SELECTED_CMDS+=("$cmd")
            fi
        done

        echo -e "\n  ${BOLD}進階 Commands:${NC}"
        for cmd in "${ADV_CMDS[@]}"; do
            echo -n -e "    啟用 ${CYAN}$cmd${NC}? [Y/n] "
            read -r yn
            if [[ "$yn" != "n" && "$yn" != "N" ]]; then
                SELECTED_CMDS+=("$cmd")
            fi
        done

        echo -e "\n  ${BOLD}Obsidian Commands:${NC}"
        for cmd in "${OBSI_CMDS[@]}"; do
            echo -n -e "    啟用 ${CYAN}$cmd${NC}? [y/N] "
            read -r yn
            if [[ "$yn" == "y" || "$yn" == "Y" ]]; then
                SELECTED_CMDS+=("$cmd")
            fi
        done

        echo -e "\n  ${GREEN}✔${NC} 將安裝 ${#SELECTED_CMDS[@]} 個 commands"
        ;;
    *)
        SELECTED_CMDS=("${CORE_CMDS[@]}")
        echo -e "\n  ${GREEN}✔${NC} 預設安裝 7 個核心 commands"
        ;;
esac

# ============================================================================
# 5) Apify Skill
# ============================================================================
print_header "步驟 4/5 — Apify 網頁爬蟲功能"

echo -e "  Apify 提供強大的網頁爬蟲 / Scraper 功能。"
echo -e "  啟用後將安裝 MCP Server 配置與 Skill 文件。"
echo -e "  ${DIM}(需要 Apify API Token，可稍後設定)${NC}"
echo ""
echo -n "  是否啟用 Apify Skill? [y/N] "
read -r APIFY_CHOICE

ENABLE_APIFY=false
if [[ "$APIFY_CHOICE" == "y" || "$APIFY_CHOICE" == "Y" ]]; then
    ENABLE_APIFY=true
    echo -e "\n  ${GREEN}✔${NC} 將安裝 Apify 配置"
else
    echo -e "\n  ${GREEN}✔${NC} 跳過 Apify"
fi

# ============================================================================
# 確認安裝
# ============================================================================
print_header "步驟 5/5 — 確認安裝"

echo -e "  目標路徑:   ${BOLD}$TARGET_DIR${NC}"
echo -e "  專案類型:   ${BOLD}$PROFILE_NAME${NC}"
echo -e "  Commands:   ${BOLD}${#SELECTED_CMDS[@]} 個${NC}"
echo -e "  Apify:      ${BOLD}$([ "$ENABLE_APIFY" = true ] && echo '啟用' || echo '未啟用')${NC}"
echo ""
echo -n -e "  確認開始安裝? [Y/n] "
read -r CONFIRM

if [[ "$CONFIRM" == "n" || "$CONFIRM" == "N" ]]; then
    print_error "安裝已取消。"
    exit 0
fi

# ============================================================================
# 6) 執行安裝
# ============================================================================
print_header "安裝中..."

# --- 建立目錄結構 ---
print_step "建立目錄結構"

mkdir -p "$TARGET_DIR/.claude/commands"
print_success ".claude/commands/"

if [[ "$ENABLE_APIFY" == true ]]; then
    mkdir -p "$TARGET_DIR/.claude/skills"
    print_success ".claude/skills/"
fi

# --- 複製 CLAUDE.md ---
print_step "安裝 CLAUDE.md"
safe_copy "$SCRIPT_DIR/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"

# --- 複製 Profile ---
if [[ -n "$PROFILE_FILE" ]]; then
    print_step "安裝 Profile: $PROFILE_NAME"
    safe_copy "$SCRIPT_DIR/$PROFILE_FILE" "$TARGET_DIR/$PROFILE_FILE"

    # 在 CLAUDE.md 末尾加上 profile 載入指令
    LOAD_LINE="請同時讀取並遵守 ${PROFILE_FILE} 中的所有規則。"
    if ! grep -qF "$LOAD_LINE" "$TARGET_DIR/CLAUDE.md" 2>/dev/null; then
        echo "" >> "$TARGET_DIR/CLAUDE.md"
        echo "$LOAD_LINE" >> "$TARGET_DIR/CLAUDE.md"
        print_success "已在 CLAUDE.md 末尾加入 Profile 載入指令"
    else
        print_info "CLAUDE.md 中已包含 Profile 載入指令，跳過"
    fi
fi

# --- 複製 Commands ---
print_step "安裝 Commands (${#SELECTED_CMDS[@]} 個)"
for cmd in "${SELECTED_CMDS[@]}"; do
    local_src="$SCRIPT_DIR/.claude/commands/${cmd}.md"
    if [[ -f "$local_src" ]]; then
        safe_copy "$local_src" "$TARGET_DIR/.claude/commands/${cmd}.md"
    else
        print_warning "找不到 command 文件: ${cmd}.md"
    fi
done

# --- 建立 session.md ---
print_step "初始化 Session 記錄"
if [[ -f "$SCRIPT_DIR/templates/session.md" ]]; then
    safe_copy "$SCRIPT_DIR/templates/session.md" "$TARGET_DIR/.claude/session.md"
else
    # 如果模板不存在，使用內建模板
    if [[ ! -f "$TARGET_DIR/.claude/session.md" ]]; then
        cat > "$TARGET_DIR/.claude/session.md" << 'SESSIONEOF'
# Session 進度記錄

## 狀態: 尚未開始
## 最後更新: -
## 當前分支: main

---

### 當前任務
- （尚未開始）

### 已完成
- （無）

### 待辦
- [ ] 初始化專案

### 決策記錄

| 日期 | 決策 | 原因 | 替代方案 |
|------|------|------|----------|
| | | | |

### 已知問題
- （無）
SESSIONEOF
        print_success "session.md (內建模板)"
    else
        print_info "session.md 已存在，跳過"
    fi
fi

# --- Apify 配置 ---
if [[ "$ENABLE_APIFY" == true ]]; then
    print_step "安裝 Apify 配置"

    # 複製 skill 文件
    if [[ -f "$SCRIPT_DIR/apify-skills/apify-ultimate-scraper.md" ]]; then
        safe_copy "$SCRIPT_DIR/apify-skills/apify-ultimate-scraper.md" \
            "$TARGET_DIR/.claude/skills/apify-ultimate-scraper.md"
    fi

    # 複製 .env.sample
    safe_copy "$SCRIPT_DIR/.claude/.env.sample" "$TARGET_DIR/.claude/.env.sample"

    # 安裝 MCP settings
    SETTINGS_FILE="$TARGET_DIR/.claude/settings.local.json"
    if [[ -f "$SCRIPT_DIR/templates/settings.apify.json" ]]; then
        safe_copy "$SCRIPT_DIR/templates/settings.apify.json" "$SETTINGS_FILE"
    fi

    print_info "請在 .claude/.env.sample 中填入你的 APIFY_TOKEN"
fi

# ============================================================================
# 7) 安裝摘要
# ============================================================================
print_header "安裝完成!"

echo ""
echo -e "  ${GREEN}已安裝到:${NC} $TARGET_DIR"
echo ""
echo -e "  ${BOLD}已安裝的文件:${NC}"
echo -e "    CLAUDE.md                        — 全局基礎配置"

if [[ -n "$PROFILE_FILE" ]]; then
    echo -e "    $PROFILE_FILE$(printf '%*s' $((33 - ${#PROFILE_FILE})) '')— $PROFILE_NAME Profile"
fi

echo -e "    .claude/session.md               — Session 進度記錄"
echo -e "    .claude/commands/ (${#SELECTED_CMDS[@]} 個)         — 自定義命令"

if [[ "$ENABLE_APIFY" == true ]]; then
    echo -e "    .claude/skills/                  — Apify Skill"
    echo -e "    .claude/settings.local.json      — MCP Server 配置"
    echo -e "    .claude/.env.sample              — 環境變數模板"
fi

echo ""
echo -e "  ${BOLD}下一步:${NC}"
echo -e "    1. cd $TARGET_DIR"
echo -e "    2. 啟動 Claude Code 開始使用"

if [[ -n "$PROFILE_FILE" ]]; then
    echo -e "    3. 修改 ${PROFILE_FILE} 中的「專案基礎資訊」"
fi

if [[ "$ENABLE_APIFY" == true ]]; then
    echo -e "    4. 在 .claude/.env.sample 中填入 APIFY_TOKEN"
fi

echo ""
echo -e "${DIM}  感謝使用 ClaudeCodePrf!${NC}"
echo ""
