"""
AI 技能分析收集器
掃描任意專案目錄，收集結構化證據，輸出一份可貼到 LLM 的分析 prompt。

用法：
    python src/ai_skill_collector.py [project_path]
    # 預設掃描當前目錄
    # 輸出 → src/output/ai_skill_prompt.md
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

# === 常量 ===
SCRIPT_DIR = Path(__file__).parent
TEMPLATE_FILE = SCRIPT_DIR / "templates" / "analysis_prompt.md"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "ai_skill_prompt.md"

# 要跳過的目錄
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "vendor", "dist", "build", ".next", ".nuxt", "Library",
    "Temp", "Logs", "obj", "bin", ".vs", ".idea",
}

# 代碼文件副檔名
CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".cs", ".php",
    ".java", ".go", ".rs", ".rb", ".swift", ".kt",
    ".c", ".cpp", ".h", ".hpp", ".lua", ".sh", ".bat",
}

# import/using 正則（用於識別技術棧）
# 注意順序：ES module from 語法要在通用 import 之前，避免誤匹配 destructuring
IMPORT_PATTERNS = [
    re.compile(r'^\s*import\s+.*?from\s+["\'](.+?)["\']', re.MULTILINE),       # ES module: import X from 'Y'
    re.compile(r'^\s*(?:const|let|var)\s+\w+\s*=\s*require\(["\'](.+?)["\']\)', re.MULTILINE),  # CJS: require('Y')
    re.compile(r"^\s*from\s+(\S+)\s+import", re.MULTILINE),                      # Python: from X import Y
    re.compile(r"^\s*import\s+([a-zA-Z_][\w.]*)\s*$", re.MULTILINE),             # Python: import X (simple)
    re.compile(r"^\s*using\s+(\S+);", re.MULTILINE),                              # C#: using X;
]

# 技術關鍵字（框架、語言、工具）
TECH_KEYWORDS = [
    "React", "Vue", "Angular", "Next.js", "Nuxt", "Svelte",
    "Django", "FastAPI", "Flask", "Express", "NestJS", "Koa",
    "Laravel", "Symfony", "CodeIgniter",
    "Unity", "Unreal", "Godot",
    "TensorFlow", "PyTorch", "scikit-learn", "LangChain", "LlamaIndex",
    "Docker", "Kubernetes", "Terraform", "Ansible",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite",
    "GraphQL", "REST", "gRPC", "WebSocket",
    "OpenAI", "Anthropic", "Claude", "GPT", "Gemini",
    "Apify", "Playwright", "Puppeteer", "Selenium",
    "Obsidian", "Notion",
]


def walk_project(root: Path):
    """遍歷專案目錄，跳過不需要的目錄，回傳所有文件 Path"""
    for dirpath, dirnames, filenames in os.walk(root):
        # 過濾掉需跳過的目錄
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            yield Path(dirpath) / fname


def build_directory_tree(root: Path, max_depth: int = 4) -> str:
    """生成目錄樹結構字串"""
    lines = [root.name + "/"]

    def _walk(path: Path, prefix: str, depth: int):
        if depth > max_depth:
            return
        try:
            entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            return

        # 過濾
        entries = [e for e in entries if e.name not in SKIP_DIRS]

        # 限制每層顯示數量，避免過長
        shown = entries[:30]
        hidden = len(entries) - len(shown)

        for i, entry in enumerate(shown):
            is_last = (i == len(shown) - 1) and hidden == 0
            connector = "└── " if is_last else "├── "
            if entry.is_dir():
                lines.append(f"{prefix}{connector}{entry.name}/")
                extension = "    " if is_last else "│   "
                _walk(entry, prefix + extension, depth + 1)
            else:
                lines.append(f"{prefix}{connector}{entry.name}")

        if hidden > 0:
            lines.append(f"{prefix}└── ... ({hidden} more items)")

    _walk(root, "", 1)
    return "\n".join(lines)


# === Tier 1: 直接技術信號 ===

def scan_profiler_files(root: Path) -> list:
    """讀取 profiler/*.md，統計行數並識別技術關鍵字"""
    results = []
    profiler_dir = root / "profiler"
    if not profiler_dir.exists():
        return results

    for md_file in sorted(profiler_dir.glob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
        except (OSError, UnicodeDecodeError):
            continue
        line_count = len(content.splitlines())
        # 識別技術關鍵字
        found_keywords = []
        for kw in TECH_KEYWORDS:
            if kw.lower() in content.lower():
                found_keywords.append(kw)
        results.append({
            "file": md_file.name,
            "lines": line_count,
            "keywords": found_keywords,
        })
    return results


def scan_claude_md(root: Path) -> dict:
    """讀取 CLAUDE.md，提取角色定義、命令列表、權限分級"""
    claude_md = root / "CLAUDE.md"
    if not claude_md.exists():
        return {}

    try:
        content = claude_md.read_text(encoding="utf-8", errors="ignore")
    except (OSError, UnicodeDecodeError):
        return {}

    line_count = len(content.splitlines())

    # 提取命令
    commands = re.findall(r"\|\s*`(\S+?)`\s*\|", content)

    # 提取角色定義
    role_match = re.search(r"身份與角色.*?\n\n(.+?)(?=\n---|\n##)", content, re.DOTALL)
    role_desc = role_match.group(1).strip() if role_match else ""

    # 檢測權限分級
    has_permission_levels = "自動同意" in content or "AUTO_APPROVE" in content

    # 識別技術關鍵字
    found_keywords = [kw for kw in TECH_KEYWORDS if kw.lower() in content.lower()]

    return {
        "exists": True,
        "lines": line_count,
        "commands": commands,
        "role_description": role_desc,
        "has_permission_levels": has_permission_levels,
        "keywords": found_keywords,
    }


def scan_spec_files(root: Path) -> list:
    """讀取 .claude/claude_specs/*.md"""
    results = []
    specs_dir = root / ".claude" / "claude_specs"
    if not specs_dir.exists():
        return results

    for md_file in sorted(specs_dir.glob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
        except (OSError, UnicodeDecodeError):
            continue
        line_count = len(content.splitlines())
        results.append({
            "file": md_file.name,
            "lines": line_count,
        })
    return results


def scan_code_imports(root: Path) -> dict:
    """掃描代碼文件的 import/using 語句，識別技術棧"""
    import_map = {}  # module_name -> count

    for fpath in walk_project(root):
        if fpath.suffix not in CODE_EXTENSIONS:
            continue
        try:
            content = fpath.read_text(encoding="utf-8", errors="ignore")
        except (OSError, UnicodeDecodeError):
            continue

        # 只讀前 100 行以提高速度
        lines = content.splitlines()[:100]
        header = "\n".join(lines)

        for pattern in IMPORT_PATTERNS:
            for match in pattern.finditer(header):
                module = match.group(1).strip().strip("'\"").split("/")[0].split(".")[0]
                if module and len(module) > 1:
                    import_map[module] = import_map.get(module, 0) + 1

    # 按頻率排序，取前 30
    sorted_imports = sorted(import_map.items(), key=lambda x: -x[1])[:30]
    return dict(sorted_imports)


def collect_tier1(root: Path) -> str:
    """收集 Tier 1 技術信號，格式化輸出"""
    sections = []

    # Profiler 文件
    profiler_data = scan_profiler_files(root)
    if profiler_data:
        sections.append("#### Profiler 文件 (`profiler/*.md`)")
        for p in profiler_data:
            kw_str = ", ".join(p["keywords"][:10]) if p["keywords"] else "（無特定關鍵字）"
            sections.append(f"- `{p['file']}`: {p['lines']} 行 | 關鍵字: {kw_str}")

    # CLAUDE.md
    claude_data = scan_claude_md(root)
    if claude_data.get("exists"):
        sections.append("\n#### CLAUDE.md 配置")
        sections.append(f"- 總行數: {claude_data['lines']}")
        if claude_data["role_description"]:
            sections.append(f"- 角色定義: {claude_data['role_description'][:200]}")
        if claude_data["commands"]:
            sections.append(f"- 自訂命令數: {len(claude_data['commands'])} 個")
            sections.append(f"- 命令列表: {', '.join(claude_data['commands'])}")
        if claude_data["has_permission_levels"]:
            sections.append("- 權限分級: 已配置（自動同意/需確認/禁止）")
        if claude_data["keywords"]:
            sections.append(f"- 技術關鍵字: {', '.join(claude_data['keywords'][:15])}")

    # 規格文件
    spec_data = scan_spec_files(root)
    if spec_data:
        sections.append("\n#### 規格文件 (`.claude/claude_specs/`)")
        for s in spec_data:
            sections.append(f"- `{s['file']}`: {s['lines']} 行")

    # 代碼 import 分析
    import_data = scan_code_imports(root)
    if import_data:
        sections.append("\n#### 代碼依賴分析（import/using 頻率 Top 30）")
        for module, count in import_data.items():
            sections.append(f"- `{module}`: {count} 次引用")

    return "\n".join(sections) if sections else "（未偵測到直接技術信號）"


# === Tier 2: AI 工具鏈成熟度 ===

def collect_tier2(root: Path) -> str:
    """收集 AI 工具鏈相關配置"""
    sections = []

    # .claude/commands/
    commands_dir = root / ".claude" / "commands"
    if commands_dir.exists():
        cmd_files = list(commands_dir.glob("*.md"))
        sections.append(f"#### 自訂命令 (`.claude/commands/`): {len(cmd_files)} 個")
        for f in sorted(cmd_files)[:20]:
            sections.append(f"- `{f.name}`")

    # .claude/skills/
    skills_dir = root / ".claude" / "skills"
    if skills_dir.exists():
        skill_files = list(skills_dir.rglob("*"))
        skill_files = [f for f in skill_files if f.is_file()]
        sections.append(f"\n#### Apify Skills (`.claude/skills/`): {len(skill_files)} 個")
        for f in sorted(skill_files)[:20]:
            rel = f.relative_to(skills_dir)
            sections.append(f"- `{rel}`")

    # settings*.json — 多模型配置
    settings_files = list(root.glob("**/settings*.json"))
    # 也檢查 .claude/ 下
    settings_files += list((root / ".claude").glob("settings*.json")) if (root / ".claude").exists() else []
    # 去重
    settings_files = list({str(f): f for f in settings_files}.values())
    if settings_files:
        sections.append(f"\n#### 設定文件: {len(settings_files)} 個")
        for sf in settings_files:
            try:
                content = sf.read_text(encoding="utf-8", errors="ignore")
            except (OSError, UnicodeDecodeError):
                continue
            # 識別模型名稱
            models = re.findall(r'"(claude-[^"]+|gpt-[^"]+|gemini[^"]*|qwen[^"]*|deepseek[^"]*)"', content, re.IGNORECASE)
            # 識別 API 端點
            endpoints = re.findall(r'"(https?://[^"]+)"', content)
            rel = sf.relative_to(root) if sf.is_relative_to(root) else sf.name
            info_parts = []
            if models:
                info_parts.append(f"模型: {', '.join(list(set(models))[:5])}")
            if endpoints:
                info_parts.append(f"端點: {len(endpoints)} 個")
            info_str = " | ".join(info_parts) if info_parts else "（無模型配置）"
            sections.append(f"- `{rel}`: {info_str}")

    # Agent 框架實驗目錄
    agent_dirs = [".junie", ".kiro", ".trae", ".agents", "agents"]
    found_agents = []
    for d in agent_dirs:
        agent_path = root / d
        if agent_path.exists():
            file_count = sum(1 for _ in agent_path.rglob("*") if _.is_file())
            found_agents.append(f"`{d}/` ({file_count} files)")
    if found_agents:
        sections.append(f"\n#### Agent 框架目錄")
        for a in found_agents:
            sections.append(f"- {a}")

    # skills-lock.json
    lock_file = root / "skills-lock.json"
    if lock_file.exists():
        try:
            content = lock_file.read_text(encoding="utf-8", errors="ignore")
            line_count = len(content.splitlines())
            sections.append(f"\n#### 依賴鎖定: `skills-lock.json` ({line_count} 行)")
        except (OSError, UnicodeDecodeError):
            pass

    # apify-skills 目錄
    apify_dir = root / "apify-skills"
    if apify_dir.exists():
        apify_files = list(apify_dir.rglob("*"))
        apify_files = [f for f in apify_files if f.is_file()]
        sections.append(f"\n#### Apify Skills 配置 (`apify-skills/`): {len(apify_files)} 個文件")

    return "\n".join(sections) if sections else "（未偵測到 AI 工具鏈配置）"


# === Tier 3: 工程成熟度 ===

def collect_tier3(root: Path) -> str:
    """收集工程成熟度指標"""
    sections = []

    # Git 歷史
    git_dir = root / ".git"
    if git_dir.exists():
        sections.append("#### Git 版本控制: 已啟用")
        # 嘗試讀取 commit 數量
        try:
            import subprocess
            result = subprocess.run(
                ["git", "log", "--oneline"],
                capture_output=True, text=True, cwd=str(root), timeout=10,
            )
            if result.returncode == 0:
                commit_count = len(result.stdout.strip().splitlines())
                sections.append(f"- 提交數: {commit_count}")

            # 分支數
            result = subprocess.run(
                ["git", "branch", "-a"],
                capture_output=True, text=True, cwd=str(root), timeout=10,
            )
            if result.returncode == 0:
                branches = [b.strip() for b in result.stdout.strip().splitlines() if b.strip()]
                sections.append(f"- 分支數: {len(branches)}")
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            sections.append("- （無法讀取 Git 歷史）")

    # 自動化安裝腳本
    setup_files = []
    for name in ["setup.sh", "setup.bat", "install.sh", "Makefile", "justfile"]:
        if (root / name).exists():
            setup_files.append(name)
    if setup_files:
        sections.append(f"\n#### 自動化腳本: {', '.join(setup_files)}")

    # 測試文件
    test_files = []
    for fpath in walk_project(root):
        fname_lower = fpath.name.lower()
        if ("test" in fname_lower or "spec" in fname_lower) and fpath.suffix in CODE_EXTENSIONS:
            test_files.append(str(fpath.relative_to(root)))
    if test_files:
        sections.append(f"\n#### 測試文件: {len(test_files)} 個")
        for t in test_files[:10]:
            sections.append(f"- `{t}`")
        if len(test_files) > 10:
            sections.append(f"- ... 還有 {len(test_files) - 10} 個")
    else:
        sections.append("\n#### 測試文件: 未偵測到")

    # CI/CD
    ci_indicators = []
    if (root / ".github").exists():
        workflows = list((root / ".github" / "workflows").glob("*.yml")) if (root / ".github" / "workflows").exists() else []
        ci_indicators.append(f"GitHub Actions ({len(workflows)} workflows)")
    if (root / ".gitlab-ci.yml").exists():
        ci_indicators.append("GitLab CI")
    if (root / "Jenkinsfile").exists():
        ci_indicators.append("Jenkins")
    if (root / ".circleci").exists():
        ci_indicators.append("CircleCI")

    if ci_indicators:
        sections.append(f"\n#### CI/CD: {', '.join(ci_indicators)}")
    else:
        sections.append("\n#### CI/CD: 未偵測到")

    # Docker
    docker_files = []
    if (root / "Dockerfile").exists():
        docker_files.append("Dockerfile")
    if (root / "docker-compose.yml").exists() or (root / "docker-compose.yaml").exists():
        docker_files.append("docker-compose")
    if (root / ".dockerignore").exists():
        docker_files.append(".dockerignore")
    if docker_files:
        sections.append(f"\n#### Docker: {', '.join(docker_files)}")

    # 套件管理
    pkg_files = []
    for name in ["package.json", "requirements.txt", "pyproject.toml", "Pipfile",
                  "composer.json", "Cargo.toml", "go.mod", "Gemfile"]:
        if (root / name).exists():
            pkg_files.append(name)
    if pkg_files:
        sections.append(f"\n#### 套件管理: {', '.join(pkg_files)}")

    return "\n".join(sections) if sections else "（未偵測到工程成熟度指標）"


# === Tier 4: 專案規模統計 ===

def collect_tier4(root: Path) -> str:
    """收集專案規模統計"""
    file_counts = {}  # extension -> count
    md_files = 0
    md_lines = 0
    code_files = 0
    code_lines = 0
    total_files = 0
    max_depth = 0

    for fpath in walk_project(root):
        total_files += 1
        ext = fpath.suffix.lower() or "(no ext)"
        file_counts[ext] = file_counts.get(ext, 0) + 1

        # 計算深度
        try:
            rel = fpath.relative_to(root)
            depth = len(rel.parts)
            if depth > max_depth:
                max_depth = depth
        except ValueError:
            pass

        # Markdown 統計
        if ext == ".md":
            md_files += 1
            try:
                content = fpath.read_text(encoding="utf-8", errors="ignore")
                md_lines += len(content.splitlines())
            except (OSError, UnicodeDecodeError):
                pass

        # 代碼統計
        if ext in CODE_EXTENSIONS:
            code_files += 1
            try:
                content = fpath.read_text(encoding="utf-8", errors="ignore")
                code_lines += len(content.splitlines())
            except (OSError, UnicodeDecodeError):
                pass

    sections = []
    sections.append(f"| 指標 | 值 |")
    sections.append(f"|------|-----|")
    sections.append(f"| 總文件數 | {total_files} |")
    sections.append(f"| Markdown 文件數 | {md_files} |")
    sections.append(f"| Markdown 總行數 | {md_lines} |")
    sections.append(f"| 代碼文件數 | {code_files} |")
    sections.append(f"| 代碼總行數 | {code_lines} |")
    sections.append(f"| 目錄最大深度 | {max_depth} |")

    # 文件類型分佈（Top 10）
    sections.append(f"\n#### 文件類型分佈（Top 10）")
    sorted_types = sorted(file_counts.items(), key=lambda x: -x[1])[:10]
    for ext, count in sorted_types:
        sections.append(f"- `{ext}`: {count} 個")

    return "\n".join(sections)


# === 組裝 Prompt ===

def load_template() -> str:
    """載入 prompt 模板"""
    if not TEMPLATE_FILE.exists():
        print(f"錯誤：找不到模板文件 {TEMPLATE_FILE}")
        sys.exit(1)
    return TEMPLATE_FILE.read_text(encoding="utf-8")


def generate_prompt(root: Path) -> str:
    """掃描專案並生成完整 prompt"""
    template = load_template()

    print("  [1/5] 建構目錄樹...")
    tree = build_directory_tree(root)

    print("  [2/5] 收集技術信號 (Tier 1)...")
    tier1 = collect_tier1(root)

    print("  [3/5] 收集 AI 工具鏈 (Tier 2)...")
    tier2 = collect_tier2(root)

    print("  [4/5] 收集工程成熟度 (Tier 3)...")
    tier3 = collect_tier3(root)

    print("  [5/5] 統計專案規模 (Tier 4)...")
    tier4 = collect_tier4(root)

    # 填入模板
    prompt = template.format(
        project_path=str(root.resolve()),
        scan_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        directory_tree=tree,
        tech_signals=tier1,
        ai_toolchain=tier2,
        engineering_maturity=tier3,
        project_stats=tier4,
    )

    return prompt


def main():
    """主函數"""
    # 解析參數
    if len(sys.argv) > 1:
        project_path = Path(sys.argv[1]).resolve()
    else:
        project_path = Path.cwd()

    if not project_path.exists():
        print(f"錯誤：路徑不存在 — {project_path}")
        sys.exit(1)

    if not project_path.is_dir():
        print(f"錯誤：不是目錄 — {project_path}")
        sys.exit(1)

    print(f"AI 技能分析收集器")
    print(f"掃描目標：{project_path}")
    print()

    prompt = generate_prompt(project_path)

    # 輸出
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(prompt, encoding="utf-8")

    line_count = len(prompt.splitlines())
    print()
    print(f"完成！已生成 {OUTPUT_FILE}")
    print(f"Prompt 共 {line_count} 行")
    print()
    print("下一步：將 ai_skill_prompt.md 的內容貼到任何 LLM 即可獲得技能分析報告。")


if __name__ == "__main__":
    main()
