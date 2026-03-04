"""
AI 技能分析可視化工具
讀取 .claude/conv/conv_aiprof.md 中的分析數據，生成互動式 HTML 報告。
"""

import os
import re
import math
from pathlib import Path

# === 設定路徑 ===
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_FILE = PROJECT_ROOT / ".claude" / "conv" / "conv_aiprof.md"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "ai_skill_report.html"


def parse_markdown(filepath: Path) -> dict:
    """解析 conv_aiprof.md，提取技能數據"""
    text = filepath.read_text(encoding="utf-8")

    # 技能維度評分映射
    level_map = {
        "頂尖": 95,
        "深入": 88,
        "系統級": 92,
        "領先": 90,
        "實戰級": 85,
        "精通": 90,
        "進階": 78,
    }

    # --- 解析第一節：六維度技能 ---
    skills = []
    section1 = re.search(r"## 一、知識面評估\s*\n(.*?)(?=\n---)", text, re.DOTALL)
    if section1:
        rows = re.findall(
            r"\|\s*\*\*(.+?)\*\*\s*\|\s*(\S+)\s*\|\s*(.+?)\s*\|",
            section1.group(1),
        )
        for name, level, evidence in rows:
            skills.append(
                {
                    "name": name,
                    "level": level,
                    "score": level_map.get(level, 70),
                    "evidence": evidence.strip(),
                }
            )

    # --- 解析排名 ---
    rank_match = re.search(r"前\s*(\d+)%", text)
    percentile = 100 - int(rank_match.group(1)) if rank_match else 95

    # --- 解析優勢 ---
    strengths = []
    strength_section = re.search(r"### 2\.1 優勢\s*\n(.*?)(?=\n###)", text, re.DOTALL)
    if strength_section:
        strengths = re.findall(
            r"-\s*\*\*(.+?)\*\*\s*—\s*(.+)", strength_section.group(1)
        )

    # --- 解析成長空間 ---
    growth = []
    growth_section = re.search(r"### 2\.2 可能的成長空間\s*\n(.*?)(?=\n---)", text, re.DOTALL)
    if growth_section:
        growth = re.findall(r"-\s*(.+)", growth_section.group(1))

    # --- 解析技術棧 ---
    tech_stack = []
    tech_section = re.search(r"### 3\.1 主要技術棧\s*\n(.*?)(?=\n###)", text, re.DOTALL)
    if tech_section:
        tech_rows = re.findall(
            r"\|\s*(\S+)\s*\|\s*(.+?)\s*\|\s*(\S+)\s*\|", tech_section.group(1)
        )
        for domain, techs, proficiency in tech_rows:
            if domain != "領域" and not domain.startswith("-"):
                tech_stack.append(
                    {
                        "domain": domain,
                        "techs": techs.strip(),
                        "proficiency": proficiency,
                        "score": level_map.get(proficiency, 70),
                    }
                )

    # --- 解析專案規模 ---
    project_stats = []
    stats_section = re.search(r"## 四、專案規模數據\s*\n(.*?)(?=\n---)", text, re.DOTALL)
    if stats_section:
        stat_rows = re.findall(
            r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|", stats_section.group(1)
        )
        for label, value in stat_rows:
            if label.strip() != "指標" and not label.strip().startswith("-"):
                project_stats.append(
                    {"label": label.strip(), "value": value.strip()}
                )

    # --- 解析總結 ---
    summary_match = re.search(r"## 五、總結\s*\n(.*?)$", text, re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else ""
    summary = re.sub(r">\s*", "", summary)

    total_score = round(sum(s["score"] for s in skills) / len(skills)) if skills else 0

    return {
        "skills": skills,
        "percentile": percentile,
        "strengths": strengths,
        "growth": growth,
        "tech_stack": tech_stack,
        "project_stats": project_stats,
        "summary": summary,
        "total_score": total_score,
    }


def generate_radar_svg(skills: list, i18n: dict = None) -> str:
    """用 SVG 繪製六維度雷達圖"""
    n = len(skills)
    if n == 0:
        return ""

    cx, cy = 200, 200
    max_r = 160
    levels = [0.2, 0.4, 0.6, 0.8, 1.0]

    svg_parts = []
    svg_parts.append(
        '<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg"'
        ' style="width:100%;max-width:420px;">'
    )

    # 背景網格
    for level in levels:
        r = max_r * level
        points = []
        for i in range(n):
            angle = (2 * math.pi * i / n) - math.pi / 2
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append(f"{x:.1f},{y:.1f}")
        svg_parts.append(
            f'<polygon points="{" ".join(points)}" '
            f'fill="none" stroke="#e2e8f0" stroke-width="1"/>'
        )

    # 軸線
    for i in range(n):
        angle = (2 * math.pi * i / n) - math.pi / 2
        x = cx + max_r * math.cos(angle)
        y = cy + max_r * math.sin(angle)
        svg_parts.append(
            f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" '
            f'stroke="#e2e8f0" stroke-width="1"/>'
        )

    # 數據多邊形
    data_points = []
    for i, skill in enumerate(skills):
        angle = (2 * math.pi * i / n) - math.pi / 2
        r = max_r * (skill["score"] / 100)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        data_points.append(f"{x:.1f},{y:.1f}")

    svg_parts.append(
        f'<polygon points="{" ".join(data_points)}" '
        f'fill="rgba(99, 102, 241, 0.25)" stroke="#6366f1" stroke-width="2.5"/>'
    )

    # 數據點 + 標籤
    for i, skill in enumerate(skills):
        angle = (2 * math.pi * i / n) - math.pi / 2
        r = max_r * (skill["score"] / 100)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        svg_parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#6366f1"/>'
        )

        # 標籤位置
        label_r = max_r + 28
        lx = cx + label_r * math.cos(angle)
        ly = cy + label_r * math.sin(angle)
        anchor = "middle"
        if math.cos(angle) > 0.3:
            anchor = "start"
        elif math.cos(angle) < -0.3:
            anchor = "end"

        name_en = i18n["skill_name"].get(skill["name"], skill["name"]) if i18n else skill["name"]
        svg_parts.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" '
            f'dominant-baseline="central" font-size="12" fill="#334155" '
            f'font-weight="600" data-zh="{skill["name"]}" data-en="{name_en}">{skill["name"]}</text>'
        )
        # 分數
        svg_parts.append(
            f'<text x="{lx:.1f}" y="{ly + 16:.1f}" text-anchor="{anchor}" '
            f'dominant-baseline="central" font-size="11" fill="#6366f1" '
            f'data-zh="{skill["score"]}分" data-en="{skill["score"]}pts">'
            f'{skill["score"]}分</text>'
        )

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def build_i18n_map(data: dict) -> dict:
    """建立中英文翻譯對照表"""
    # 技能名稱翻譯
    skill_name_en = {
        "LLM 生態理解": "LLM Ecosystem",
        "AI Agent 架構": "AI Agent Architecture",
        "Prompt Engineering": "Prompt Engineering",
        "AI 輔助開發工作流": "AI-Assisted Dev Workflow",
        "多模型策略": "Multi-Model Strategy",
        "AI/ML 實作能力": "AI/ML Implementation",
    }
    # 等級翻譯
    level_en = {
        "頂尖": "Top-tier",
        "深入": "Deep",
        "系統級": "System-level",
        "領先": "Leading",
        "實戰級": "Production-grade",
        "精通": "Expert",
        "進階": "Advanced",
    }
    # 領域翻譯
    domain_en = {
        "後端": "Backend",
        "前端": "Frontend",
        "遊戲開發": "Game Dev",
        "資料庫": "Database",
        "DevOps": "DevOps",
        "知識管理": "Knowledge Mgmt",
    }
    # 統計標籤翻譯
    stat_en = {
        "Markdown 文件數": "Markdown Files",
        "總文件數": "Total Files",
        "配置與規格總行數": "Config & Spec Lines",
        "Profile 文件總行數": "Profile Lines",
        "ADGC 規格書": "ADGC Spec",
        "自訂命令": "Custom Commands",
        "Apify Skills": "Apify Skills",
        "Agent 目錄": "Agent Directories",
    }
    return {
        "skill_name": skill_name_en,
        "level": level_en,
        "domain": domain_en,
        "stat": stat_en,
    }


def generate_html(data: dict, i18n: dict) -> str:
    """生成完整 HTML 報告（含 i18n 支援）"""
    radar_svg = generate_radar_svg(data["skills"], i18n)

    # 技能卡片
    skill_cards = ""
    for s in data["skills"]:
        bar_color = "#6366f1" if s["score"] >= 90 else "#8b5cf6" if s["score"] >= 80 else "#a78bfa"
        name_en = i18n["skill_name"].get(s["name"], s["name"])
        level_en = i18n["level"].get(s["level"], s["level"])
        skill_cards += f"""
        <div class="card skill-card">
          <div class="skill-header">
            <span class="skill-name" data-zh="{s["name"]}" data-en="{name_en}">{s["name"]}</span>
            <span class="skill-badge" data-zh="{s["level"]}" data-en="{level_en}">{s["level"]}</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" style="width:{s["score"]}%;background:{bar_color}"></div>
          </div>
          <div class="skill-score">{s["score"]}/100</div>
          <div class="skill-evidence">{s["evidence"]}</div>
        </div>"""

    # 優勢列表 — 英文翻譯
    strength_en_map = {
        "AI 工具鏈整合能力": ("AI Toolchain Integration",
            "Most programmers are still 'asking ChatGPT questions'; the author is designing reusable AI dev frameworks"),
        "跨領域覆蓋": ("Cross-Domain Coverage",
            "Proficient in Unity/C#, PHP/Laravel, Python/FastAPI, and Obsidian automation — rare breadth"),
        "工程化思維": ("Engineering Mindset",
            "ADGC spec with 1600 lines, deterministic simulation, ECS architecture, DDD/CQRS — not beginner-level work"),
        "中國 + 國際 AI 生態雙棲": ("Dual CN + International AI Ecosystem",
            "Familiar with both Anthropic/OpenAI and Alibaba/Zhipu model ecosystems — globally rare"),
    }
    strength_html = ""
    for title, desc in data["strengths"]:
        en_title, en_desc = strength_en_map.get(title, (title, desc))
        strength_html += f"""
        <div class="strength-item">
          <div class="strength-title" data-zh="{title}" data-en="{en_title}">{title}</div>
          <div class="strength-desc" data-zh="{desc}" data-en="{en_desc}">{desc}</div>
        </div>"""

    # 成長建議
    growth_en_list = [
        'Currently focused on <strong>configuration & architecture design</strong>; no evidence of hands-on AI/ML model training, fine-tuning, or RAG pipeline building',
        'Many Apify skills reference existing actors; unclear if custom actors or scrapers have been developed',
        'No test code or CI/CD pipeline found; actual application code is not in this repo, so coding ability ceiling is unknown',
    ]
    growth_html = ""
    for idx, item in enumerate(data["growth"]):
        clean = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", item)
        en_text = growth_en_list[idx] if idx < len(growth_en_list) else clean
        growth_html += f'<div class="growth-item" data-zh="{clean}" data-en="{en_text}">{clean}</div>'

    # 技術棧
    tech_html = ""
    for t in data["tech_stack"]:
        bar_color = "#10b981" if t["score"] >= 90 else "#34d399" if t["score"] >= 80 else "#6ee7b7"
        domain_en = i18n["domain"].get(t["domain"], t["domain"])
        prof_en = i18n["level"].get(t["proficiency"], t["proficiency"])
        tech_html += f"""
        <div class="tech-row">
          <span class="tech-domain" data-zh="{t["domain"]}" data-en="{domain_en}">{t["domain"]}</span>
          <span class="tech-names">{t["techs"]}</span>
          <div class="tech-bar-wrap">
            <div class="tech-bar" style="width:{t["score"]}%;background:{bar_color}"></div>
          </div>
          <span class="tech-prof" data-zh="{t["proficiency"]}" data-en="{prof_en}">{t["proficiency"]}</span>
        </div>"""

    # 專案統計
    stats_html = ""
    for st in data["project_stats"]:
        label_en = i18n["stat"].get(st["label"], st["label"])
        stats_html += f"""
        <div class="stat-item">
          <div class="stat-value">{st["value"]}</div>
          <div class="stat-label" data-zh="{st["label"]}" data-en="{label_en}">{st["label"]}</div>
        </div>"""

    # 排名視覺化
    rank_pos = 100 - data["percentile"]

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title data-zh="AI 技能分析報告" data-en="AI Skill Analysis Report">AI 技能分析報告</title>
<style>
  :root {{
    --bg: #0f172a;
    --surface: #1e293b;
    --surface2: #334155;
    --text: #f1f5f9;
    --text2: #94a3b8;
    --accent: #6366f1;
    --accent2: #818cf8;
    --green: #10b981;
    --radius: 16px;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    padding: 24px;
  }}
  .container {{ max-width: 1100px; margin: 0 auto; }}

  /* 標題區 */
  .hero {{
    text-align: center;
    padding: 48px 24px 32px;
    background: linear-gradient(135deg, #1e1b4b, #312e81, #1e293b);
    border-radius: var(--radius);
    margin-bottom: 24px;
  }}
  .hero h1 {{ font-size: 2rem; margin-bottom: 8px; }}
  .hero .subtitle {{ color: var(--text2); font-size: 1rem; }}
  .hero .total-score {{
    display: inline-block;
    margin-top: 20px;
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .hero .score-label {{ color: var(--text2); font-size: 0.9rem; margin-top: -4px; }}

  /* 卡片 */
  .card {{
    background: var(--surface);
    border-radius: var(--radius);
    padding: 24px;
    margin-bottom: 20px;
  }}
  .card h2 {{
    font-size: 1.25rem;
    margin-bottom: 16px;
    color: var(--accent2);
  }}

  /* 排名條 */
  .rank-section {{
    display: flex;
    align-items: center;
    gap: 24px;
    flex-wrap: wrap;
  }}
  .rank-bar-container {{
    flex: 1;
    min-width: 280px;
    position: relative;
    height: 40px;
    background: linear-gradient(90deg, #ef4444, #f59e0b, #10b981, #06b6d4);
    border-radius: 20px;
    overflow: visible;
  }}
  .rank-marker {{
    position: absolute;
    top: -8px;
    width: 4px;
    height: 56px;
    background: white;
    border-radius: 2px;
    transition: left 1s ease;
  }}
  .rank-labels {{
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
    font-size: 0.75rem;
    color: var(--text2);
  }}
  .rank-text {{
    font-size: 2rem;
    font-weight: 700;
    color: var(--green);
    white-space: nowrap;
  }}
  .rank-desc {{ color: var(--text2); font-size: 0.85rem; }}

  /* 雷達圖區 */
  .radar-wrap {{
    display: flex;
    justify-content: center;
    padding: 16px 0;
  }}
  .radar-wrap svg text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}

  /* 技能卡片 */
  .skills-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 16px;
  }}
  .skill-card {{
    margin-bottom: 0;
    transition: transform 0.2s;
  }}
  .skill-card:hover {{ transform: translateY(-2px); }}
  .skill-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }}
  .skill-name {{ font-weight: 700; font-size: 1rem; }}
  .skill-badge {{
    background: var(--accent);
    color: white;
    padding: 2px 12px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
  }}
  .progress-bar {{
    height: 8px;
    background: var(--surface2);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 8px;
  }}
  .progress-fill {{
    height: 100%;
    border-radius: 4px;
    transition: width 1.2s ease;
  }}
  .skill-score {{ font-size: 0.85rem; color: var(--accent2); margin-bottom: 8px; }}
  .skill-evidence {{ font-size: 0.82rem; color: var(--text2); line-height: 1.5; }}

  /* 優勢 */
  .strength-item {{
    padding: 16px;
    background: var(--surface2);
    border-radius: 12px;
    margin-bottom: 12px;
    border-left: 4px solid var(--accent);
  }}
  .strength-title {{ font-weight: 700; margin-bottom: 4px; }}
  .strength-desc {{ font-size: 0.9rem; color: var(--text2); }}

  /* 成長建議 */
  .growth-item {{
    padding: 14px 16px;
    background: var(--surface2);
    border-radius: 12px;
    margin-bottom: 10px;
    border-left: 4px solid #f59e0b;
    font-size: 0.9rem;
    color: var(--text2);
  }}
  .growth-item strong {{ color: var(--text); }}

  /* 技術棧 */
  .tech-row {{
    display: grid;
    grid-template-columns: 80px 1fr 120px 60px;
    gap: 12px;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid var(--surface2);
  }}
  .tech-domain {{ font-weight: 600; font-size: 0.85rem; }}
  .tech-names {{ font-size: 0.85rem; color: var(--text2); }}
  .tech-bar-wrap {{
    height: 6px;
    background: var(--surface2);
    border-radius: 3px;
    overflow: hidden;
  }}
  .tech-bar {{
    height: 100%;
    border-radius: 3px;
    transition: width 1s ease;
  }}
  .tech-prof {{ font-size: 0.8rem; color: var(--green); text-align: right; }}

  /* 統計 */
  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 16px;
  }}
  .stat-item {{
    text-align: center;
    padding: 16px;
    background: var(--surface2);
    border-radius: 12px;
  }}
  .stat-value {{ font-size: 1.4rem; font-weight: 700; color: var(--accent2); }}
  .stat-label {{ font-size: 0.8rem; color: var(--text2); margin-top: 4px; }}

  /* 總結 */
  .summary {{ font-size: 1rem; color: var(--text2); line-height: 1.8; }}
  .summary strong {{ color: var(--text); }}

  /* 頁尾 */
  .footer {{
    text-align: center;
    padding: 32px 0 16px;
    color: var(--surface2);
    font-size: 0.8rem;
  }}

  /* 語言切換按鈕 */
  .lang-toggle {{
    position: fixed;
    top: 16px;
    right: 16px;
    background: var(--surface);
    border: 1px solid var(--surface2);
    color: var(--text);
    padding: 6px 14px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.85rem;
    z-index: 100;
    transition: background 0.2s;
  }}
  .lang-toggle:hover {{ background: var(--surface2); }}

  /* 動畫 */
  .fade-in {{
    opacity: 0;
    transform: translateY(20px);
    animation: fadeUp 0.6s ease forwards;
  }}
  @keyframes fadeUp {{
    to {{ opacity: 1; transform: translateY(0); }}
  }}
  .delay-1 {{ animation-delay: 0.1s; }}
  .delay-2 {{ animation-delay: 0.2s; }}
  .delay-3 {{ animation-delay: 0.3s; }}
  .delay-4 {{ animation-delay: 0.4s; }}
  .delay-5 {{ animation-delay: 0.5s; }}
  .delay-6 {{ animation-delay: 0.6s; }}

  /* RWD */
  @media (max-width: 640px) {{
    body {{ padding: 12px; }}
    .hero h1 {{ font-size: 1.4rem; }}
    .hero .total-score {{ font-size: 2.5rem; }}
    .rank-section {{ flex-direction: column; }}
    .tech-row {{ grid-template-columns: 1fr; gap: 4px; }}
  }}
</style>
</head>
<body>
<button class="lang-toggle" onclick="toggleLang()" id="langBtn">EN</button>
<div class="container">

  <!-- 標題 -->
  <div class="hero fade-in">
    <h1 data-zh="AI 技能分析報告" data-en="AI Skill Analysis Report">AI 技能分析報告</h1>
    <div class="subtitle" data-zh="基於 ClaudeCodePrf 專案的技術畫像評估" data-en="Technical profile assessment based on ClaudeCodePrf project">基於 ClaudeCodePrf 專案的技術畫像評估</div>
    <div class="total-score">{data["total_score"]}</div>
    <div class="score-label" data-zh="綜合評分（滿分 100）" data-en="Overall Score (out of 100)">綜合評分（滿分 100）</div>
  </div>

  <!-- 全球排名 -->
  <div class="card fade-in delay-1">
    <h2 data-zh="全球排名" data-en="Global Ranking">全球排名</h2>
    <div class="rank-section">
      <div style="min-width:120px">
        <div class="rank-text">Top {100 - data["percentile"]}%</div>
        <div class="rank-desc" data-zh="全球程序員排名" data-en="Global developer ranking">全球程序員排名</div>
      </div>
      <div style="flex:1;min-width:280px">
        <div class="rank-bar-container">
          <div class="rank-marker" style="left:{rank_pos}%"></div>
        </div>
        <div class="rank-labels">
          <span>Top 1%</span><span>Top 25%</span><span>Top 50%</span><span>Top 75%</span><span>100%</span>
        </div>
      </div>
    </div>
  </div>

  <!-- 雷達圖 -->
  <div class="card fade-in delay-2">
    <h2 data-zh="AI 技能雷達圖" data-en="AI Skill Radar Chart">AI 技能雷達圖</h2>
    <div class="radar-wrap">
      {radar_svg}
    </div>
  </div>

  <!-- 各維度評分 -->
  <div class="fade-in delay-3">
    <div class="card" style="margin-bottom:16px"><h2 data-zh="技能維度詳情" data-en="Skill Dimension Details">技能維度詳情</h2></div>
    <div class="skills-grid">
      {skill_cards}
    </div>
  </div>

  <!-- 優勢 -->
  <div class="card fade-in delay-4" style="margin-top:20px">
    <h2 data-zh="核心優勢" data-en="Core Strengths">核心優勢</h2>
    {strength_html}
  </div>

  <!-- 成長建議 -->
  <div class="card fade-in delay-5">
    <h2 data-zh="成長空間與建議" data-en="Growth Areas & Recommendations">成長空間與建議</h2>
    {growth_html}
  </div>

  <!-- 技術棧 -->
  <div class="card fade-in delay-5">
    <h2 data-zh="技術棧總覽" data-en="Tech Stack Overview">技術棧總覽</h2>
    {tech_html}
  </div>

  <!-- 專案統計 -->
  <div class="card fade-in delay-6">
    <h2 data-zh="專案規模" data-en="Project Scale">專案規模</h2>
    <div class="stats-grid">
      {stats_html}
    </div>
  </div>

  <!-- 總結 -->
  <div class="card fade-in delay-6">
    <h2 data-zh="總結" data-en="Summary">總結</h2>
    <div class="summary" data-zh="{data["summary"]}" data-en="AI Toolchain Architect — not someone who builds AI, but someone who leverages AI to the fullest. This positioning is highly valuable in today's market, as most companies lack not AI researchers, but people who can integrate AI into development workflows.">{data["summary"]}</div>
  </div>

  <div class="footer">Generated by AI Skill Analyzer &middot; {__import__('datetime').date.today().isoformat()}</div>
</div>

<script>
// i18n：語言切換
let currentLang = 'zh';

function detectLang() {{
  const lang = navigator.language || navigator.userLanguage || 'zh';
  return lang.startsWith('zh') ? 'zh' : 'en';
}}

function applyLang(lang) {{
  currentLang = lang;
  document.querySelectorAll('[data-' + lang + ']').forEach(el => {{
    const text = el.getAttribute('data-' + lang);
    if (text) el.innerHTML = text;
  }});
  // 更新雷達圖 SVG 文字
  document.querySelectorAll('svg text[data-' + lang + ']').forEach(el => {{
    const text = el.getAttribute('data-' + lang);
    if (text) el.textContent = text;
  }});
  document.getElementById('langBtn').textContent = lang === 'zh' ? 'EN' : '中文';
  document.documentElement.lang = lang === 'zh' ? 'zh-TW' : 'en';
}}

function toggleLang() {{
  applyLang(currentLang === 'zh' ? 'en' : 'zh');
}}

// 進度條動畫 + 語言偵測
document.addEventListener('DOMContentLoaded', () => {{
  // 進度條動畫
  document.querySelectorAll('.progress-fill, .tech-bar').forEach(el => {{
    const w = el.style.width;
    el.style.width = '0%';
    requestAnimationFrame(() => {{
      requestAnimationFrame(() => {{ el.style.width = w; }});
    }});
  }});
  // 自動偵測語言
  const detectedLang = detectLang();
  if (detectedLang !== 'zh') {{
    applyLang(detectedLang);
  }}
}});
</script>
</body>
</html>"""
    return html


def main():
    """主函數"""
    if not DATA_FILE.exists():
        print(f"錯誤：找不到數據文件 {DATA_FILE}")
        return

    print(f"讀取數據：{DATA_FILE}")
    data = parse_markdown(DATA_FILE)

    print(f"解析到 {len(data['skills'])} 個技能維度")
    print(f"綜合評分：{data['total_score']}/100")
    print(f"全球排名：Top {100 - data['percentile']}%")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    i18n = build_i18n_map(data)
    html = generate_html(data, i18n)
    OUTPUT_FILE.write_text(html, encoding="utf-8")
    print(f"報告已生成：{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
