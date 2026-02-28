import { useState } from "react";

const models = [
  {
    id: "qwen35",
    name: "Qwen 3.5",
    maker: "Alibaba / 通義千問",
    tagline: "開源 MoE 多模態旗艦",
    accent: "#6366F1",
    icon: "🌐",
    params: "397B 總量 / 17B 激活",
    arch: "MoE (512 experts, 10+1 activated)",
    context: "262K（Plus 版 1M）",
    license: "Apache 2.0（完全開源）",
    apiPrice: { input: "~$0.8", output: "~$2.5", note: "Plus 版經 Alibaba Cloud 付費使用" },
    released: "2026-02-16",
    features: [
      "原生多模態（文字+圖片+影片 early fusion）",
      "Gated Delta Networks + MoE 混合架構",
      "201 種語言支援",
      "Thinking / Fast 雙模式",
      "原生 Tool Use & Function Calling",
      "Qwen Code CLI 終端工具",
      "可本地部署（vLLM / SGLang）",
    ],
    strengths: ["開源最強多模態之一", "推理成本極低（17B 激活）", "多語言覆蓋最廣", "可完全自建部署"],
    weaknesses: ["推理速度受 MoE 架構影響", "生態系成熟度不如 OpenAI / Anthropic", "Alibaba 雲端服務在海外體驗較差"],
    bestFor: ["需要開源 & 自部署的企業", "多模態（圖片/影片分析）任務", "多語言 & 亞洲市場應用"],
    verdict: "開源多模態王者",
  },
  {
    id: "claude",
    name: "Claude",
    maker: "Anthropic",
    tagline: "安全可靠的推理專家",
    accent: "#D97706",
    icon: "🧠",
    params: "未公開",
    arch: "Dense Transformer（推測）",
    context: "200K 標準 / 1M Beta",
    license: "閉源（API / 訂閱制）",
    apiPrice: { input: "$3~5", output: "$15~25", note: "Haiku $1/$5 · Sonnet $3/$15 · Opus $5/$25" },
    released: "Opus 4.6: 2026-02-05 · Sonnet 4.6: 2026-02-18",
    features: [
      "三級模型線：Haiku / Sonnet / Opus",
      "Extended Thinking 深度推理",
      "1M token 上下文（Beta）",
      "Agent Teams 多代理協作",
      "Claude Code CLI 終端工具",
      "Computer Use 操控電腦",
      "Prompt Caching 最高省 90%",
      "Constitutional AI 安全設計",
    ],
    strengths: ["推理 & 程式碼品質業界頂尖", "安全性與拒絕率業界最佳", "Claude Code 生態成熟（$1B+ ARR）", "Sonnet 4.6 性價比極高"],
    weaknesses: ["Opus 定價偏高（$5/$25）", "不開源，無法自部署", "訂閱制有用量限制（每 5 小時 reset）"],
    bestFor: ["追求最高推理品質", "企業級安全合規需求", "Agentic coding 重度使用者"],
    verdict: "推理品質天花板",
  },
  {
    id: "kimi",
    name: "Kimi K2.5",
    maker: "Moonshot AI / 月之暗面",
    tagline: "Agent Swarm 平行作戰",
    accent: "#10B981",
    icon: "🐝",
    params: "1T 總量 / 32B 激活",
    arch: "MoE (384 experts, 8 activated)",
    context: "256K",
    license: "Modified MIT（開源可商用）",
    apiPrice: { input: "$0.60", output: "$3.00", note: "Cache: $0.10/M｜Kimi Code: $15-200/月" },
    released: "2026-01-27",
    features: [
      "Agent Swarm：最多 100 個平行子代理",
      "原生多模態（15T 混合視覺/文字訓練）",
      "四種模式：Instant / Thinking / Agent / Swarm",
      "Kimi Code CLI（類似 Claude Code）",
      "UI-to-Code & 視覺除錯",
      "影片理解能力",
      "Parallel-Agent RL 訓練技術",
    ],
    strengths: ["Agent Swarm 獨家平行代理（4.5x 加速）", "API 定價極具競爭力", "前端開發 & UI-to-Code 特別強", "開源可商用"],
    weaknesses: ["Swarm 模式的實際成本不透明", "情境感知力不如 Claude/GPT", "生態系與工具鏈仍在建設中"],
    bestFor: ["需要大規模平行任務處理", "前端開發 & UI 設計轉程式碼", "追求極致 API 成本效益"],
    verdict: "平行代理先驅",
  },
  {
    id: "codex",
    name: "GPT-5.3 Codex",
    maker: "OpenAI",
    tagline: "最強 Agentic 程式碼引擎",
    accent: "#EF4444",
    icon: "⚙️",
    params: "未公開",
    arch: "未公開（推測 MoE）",
    context: "200K（輸出最高 128K）",
    license: "閉源（ChatGPT 訂閱 / API）",
    apiPrice: { input: "$2", output: "$10", note: "經 ChatGPT Plus $20/月 或 Pro $200/月 使用" },
    released: "2026-02-05",
    features: [
      "Codex App + CLI + IDE Extension 全平台",
      "長時間自主執行（小時/天級任務）",
      "即時互動：任務執行中可引導修正",
      "Codex-Spark：>1000 tok/s 超低延遲",
      "GitHub 深度整合（PR Review、Coding Agent）",
      "SWE-Bench Pro SOTA",
      "首個達 High 網安風險等級的模型",
    ],
    strengths: ["Agentic coding 能力最強", "長時間自主任務業界領先", "GitHub 生態整合最深", "多模型切換（Codex/GPT-5.2）"],
    weaknesses: ["API 定價尚未完全公開", "網安風險等級引發安全疑慮", "需 ChatGPT 付費訂閱才能使用", "用量以 credit 計費，消耗不易預測"],
    bestFor: ["專業軟體工程團隊", "長時間自主 coding 任務", "GitHub 重度使用者"],
    verdict: "程式碼之王",
  },
  {
    id: "antigravity",
    name: "Antigravity",
    maker: "Google",
    tagline: "Agent-First IDE 平台",
    accent: "#3B82F6",
    icon: "🚀",
    params: "Gemini 3 Pro（主力模型）",
    arch: "基於 VS Code fork 的 IDE + Gemini 3",
    context: "依模型而定（Gemini 3 Pro 最高 2M）",
    license: "免費公開預覽（2026 預計推出付費方案）",
    apiPrice: { input: "免費*", output: "免費*", note: "公開預覽期免費｜支援 Claude Sonnet 4.5 / GPT-OSS" },
    released: "2025-11-18（公開預覽）",
    features: [
      "Agent Manager：多代理平行調度中心",
      "Editor View + Manager Surface 雙模式",
      "內建瀏覽器自動化（Chrome 控制）",
      "支援多模型（Gemini 3 / Claude / GPT-OSS）",
      "Skills 自訂代理行為規則",
      "Google Cloud 原生整合（Cloud Run、Firebase）",
      "VS Code 擴充套件相容",
    ],
    strengths: ["目前完全免費使用", "多代理平行調度獨家功能", "瀏覽器自動化能力獨一無二", "Google 生態系深度整合"],
    weaknesses: ["仍在預覽階段，穩定性待驗證", "長上下文記憶消耗大量資源（卡頓問題）", "未來定價不確定", "重度偏向 Google Cloud"],
    bestFor: ["想免費體驗 Agent-First IDE", "Google Cloud 使用者", "需要瀏覽器自動化測試的開發者"],
    verdict: "免費 Agent IDE 新星",
  },
  {
    id: "glm5",
    name: "GLM-5",
    maker: "Zhipu AI / 智譜清言",
    tagline: "華為晶片的開源旗艦",
    accent: "#F59E0B",
    icon: "🐴",
    params: "744B 總量 / 44B 激活",
    arch: "MoE (256 experts, 8 activated)",
    context: "200K",
    license: "MIT（完全開源可商用）",
    apiPrice: { input: "$1.00", output: "$3.20", note: "比 Claude Opus 便宜 5-8 倍" },
    released: "2026-02-11",
    features: [
      "100% 華為昇騰晶片訓練（零 NVIDIA）",
      "Agent Mode：自主產生辦公文件",
      "Slime 異步 RL 框架（APRIL 技術）",
      "幻覺率業界最低（AA Omniscience Index -1）",
      "SWE-bench Verified 77.8%",
      "GLM Coding Plan（中國版 Claude Code）",
      "支援 7 款國產晶片推理",
    ],
    strengths: ["開源最強之一（MIT License）", "幻覺率業界最低", "API 定價極具競爭力", "完全國產自主（對地緣政治敏感者重要）"],
    weaknesses: ["推理速度較慢（~17 tok/s vs NVIDIA 25+）", "Coding Plan 已漲價 30-60%", "英文生態系工具整合較弱", "情境感知力被指不如 Claude"],
    bestFor: ["需要低幻覺率的知識密集應用", "預算有限但需要前沿性能", "中國市場 & 國產化需求"],
    verdict: "國產晶片奇蹟",
  },
];

const aspects = [
  { key: "overview", label: "📊 總覽", icon: "📊" },
  { key: "pricing", label: "💰 價格", icon: "💰" },
  { key: "features", label: "⚡ 能力", icon: "⚡" },
  { key: "audience", label: "🎯 選擇", icon: "🎯" },
];

export default function ModelComparison() {
  const [selectedModel, setSelectedModel] = useState(null);
  const [activeAspect, setActiveAspect] = useState("overview");

  const filtered = selectedModel ? models.filter(m => m.id === selectedModel) : models;

  return (
    <div style={{
      fontFamily: "'Noto Sans TC', 'SF Pro Display', -apple-system, sans-serif",
      background: "#08080C",
      color: "#E0DDD8",
      minHeight: "100vh",
      overflow: "auto",
    }}>
      <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet" />

      {/* Header */}
      <div style={{
        padding: "36px 20px 20px",
        textAlign: "center",
        borderBottom: "1px solid rgba(255,255,255,0.05)",
        background: "linear-gradient(180deg, rgba(255,255,255,0.02) 0%, transparent 100%)",
      }}>
        <div style={{
          fontSize: "10px", fontFamily: "'JetBrains Mono', monospace",
          color: "#555", letterSpacing: "3px", textTransform: "uppercase", marginBottom: "10px",
        }}>
          AI Foundation Models · 2026 Q1
        </div>
        <h1 style={{
          fontSize: "clamp(22px, 5vw, 32px)", fontWeight: 900, margin: "0 0 6px", lineHeight: 1.2,
          background: "linear-gradient(135deg, #fff 0%, #888 100%)",
          WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
        }}>
          AI 模型大比拼
        </h1>
        <p style={{ color: "#666", fontSize: "13px", margin: 0 }}>
          繁體中文工程師視角 · 6 款前沿模型完整比較
        </p>
      </div>

      {/* Model Selector */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(100px, 1fr))",
        gap: "6px", padding: "16px 12px 8px", maxWidth: "820px", margin: "0 auto",
      }}>
        {models.map(m => (
          <button key={m.id} onClick={() => setSelectedModel(selectedModel === m.id ? null : m.id)}
            style={{
              background: selectedModel === m.id ? `rgba(255,255,255,0.06)` : "rgba(255,255,255,0.02)",
              border: selectedModel === m.id ? `1.5px solid ${m.accent}` : "1.5px solid rgba(255,255,255,0.06)",
              borderRadius: "10px", padding: "10px 6px", cursor: "pointer",
              transition: "all 0.15s ease", textAlign: "center", color: "#E0DDD8",
            }}>
            <div style={{ fontSize: "20px", marginBottom: "3px" }}>{m.icon}</div>
            <div style={{
              fontSize: "12px", fontWeight: 700,
              color: selectedModel === m.id ? m.accent : "#ccc",
              lineHeight: 1.2,
            }}>{m.name}</div>
            <div style={{
              fontSize: "9px", fontFamily: "'JetBrains Mono', monospace",
              color: "#555", marginTop: "2px",
            }}>{m.maker.split(' / ')[0]}</div>
          </button>
        ))}
      </div>

      {/* Aspect Tabs */}
      <div style={{ display: "flex", justifyContent: "center", gap: "3px", padding: "6px 12px 14px" }}>
        {aspects.map(a => (
          <button key={a.key} onClick={() => setActiveAspect(a.key)}
            style={{
              background: activeAspect === a.key ? "rgba(255,255,255,0.08)" : "transparent",
              border: activeAspect === a.key ? "1px solid rgba(255,255,255,0.12)" : "1px solid transparent",
              borderRadius: "7px", padding: "6px 14px",
              color: activeAspect === a.key ? "#fff" : "#666",
              fontSize: "12px", fontWeight: 500, cursor: "pointer", transition: "all 0.15s ease",
              fontFamily: "'Noto Sans TC', sans-serif",
            }}>{a.label}</button>
        ))}
      </div>

      {/* Content */}
      <div style={{ padding: "0 12px 40px", maxWidth: "820px", margin: "0 auto" }}>

        {/* Overview */}
        {activeAspect === "overview" && (
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {filtered.map(m => (
              <div key={m.id} style={{
                background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)",
                borderRadius: "12px", overflow: "hidden",
              }}>
                <div style={{
                  padding: "14px 16px", borderBottom: "1px solid rgba(255,255,255,0.04)",
                  display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap",
                }}>
                  <span style={{ fontSize: "18px" }}>{m.icon}</span>
                  <span style={{ fontWeight: 700, fontSize: "15px", color: m.accent }}>{m.name}</span>
                  <span style={{
                    fontSize: "10px", fontFamily: "'JetBrains Mono', monospace",
                    background: "rgba(255,255,255,0.05)", padding: "2px 8px", borderRadius: "4px", color: "#888",
                  }}>{m.tagline}</span>
                  <span style={{
                    marginLeft: "auto", fontSize: "11px", fontWeight: 700, color: m.accent,
                    background: `${m.accent}15`, padding: "3px 10px", borderRadius: "6px",
                  }}>{m.verdict}</span>
                </div>
                <div style={{
                  display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
                  gap: "1px", background: "rgba(255,255,255,0.02)",
                }}>
                  {[
                    ["參數量", m.params],
                    ["架構", m.arch],
                    ["上下文", m.context],
                    ["授權", m.license],
                    ["發布日", m.released],
                    ["API 輸入/輸出", `${m.apiPrice.input} / ${m.apiPrice.output} per 1M tok`],
                  ].map(([label, val], i) => (
                    <div key={i} style={{ padding: "10px 14px", background: "#08080C" }}>
                      <div style={{ fontSize: "10px", color: "#666", marginBottom: "3px", fontWeight: 600 }}>{label}</div>
                      <div style={{ fontSize: "12px", color: "#bbb", lineHeight: 1.4, fontFamily: "'JetBrains Mono', monospace" }}>{val}</div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pricing */}
        {activeAspect === "pricing" && (
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {/* Price bar chart */}
            <div style={{
              background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)",
              borderRadius: "12px", padding: "16px",
            }}>
              <div style={{ fontSize: "12px", fontWeight: 600, color: "#888", marginBottom: "14px" }}>
                💰 API 輸入價格比較（$/1M tokens）
              </div>
              {[
                { name: "Kimi K2.5", price: 0.60, color: "#10B981" },
                { name: "Qwen 3.5+", price: 0.80, color: "#6366F1" },
                { name: "GLM-5", price: 1.00, color: "#F59E0B" },
                { name: "Haiku 4.5", price: 1.00, color: "#D97706" },
                { name: "Codex 5.3", price: 2.00, color: "#EF4444" },
                { name: "Sonnet 4.6", price: 3.00, color: "#D97706" },
                { name: "Opus 4.6", price: 5.00, color: "#D97706" },
              ].map((item, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "5px" }}>
                  <div style={{
                    width: "85px", fontSize: "10px", fontFamily: "'JetBrains Mono', monospace",
                    color: "#999", textAlign: "right", flexShrink: 0,
                  }}>{item.name}</div>
                  <div style={{
                    flex: 1, background: "rgba(255,255,255,0.03)", borderRadius: "3px", height: "16px",
                    overflow: "hidden",
                  }}>
                    <div style={{
                      width: `${(item.price / 5) * 100}%`, height: "100%",
                      background: `linear-gradient(90deg, ${item.color}44, ${item.color}88)`,
                      borderRadius: "3px", display: "flex", alignItems: "center",
                      justifyContent: "flex-end", paddingRight: "5px", minWidth: "30px",
                    }}>
                      <span style={{ fontSize: "9px", fontFamily: "'JetBrains Mono', monospace", color: "#fff", fontWeight: 600 }}>
                        ${item.price}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
              <div style={{ fontSize: "10px", color: "#555", marginTop: "10px", fontStyle: "italic" }}>
                * Antigravity 公開預覽期免費，未列入｜價格以官方公告為準
              </div>
            </div>

            {/* Output price chart */}
            <div style={{
              background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)",
              borderRadius: "12px", padding: "16px",
            }}>
              <div style={{ fontSize: "12px", fontWeight: 600, color: "#888", marginBottom: "14px" }}>
                💰 API 輸出價格比較（$/1M tokens）
              </div>
              {[
                { name: "Qwen 3.5+", price: 2.50, color: "#6366F1" },
                { name: "Kimi K2.5", price: 3.00, color: "#10B981" },
                { name: "GLM-5", price: 3.20, color: "#F59E0B" },
                { name: "Haiku 4.5", price: 5.00, color: "#D97706" },
                { name: "Codex 5.3", price: 10.00, color: "#EF4444" },
                { name: "Sonnet 4.6", price: 15.00, color: "#D97706" },
                { name: "Opus 4.6", price: 25.00, color: "#D97706" },
              ].map((item, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "5px" }}>
                  <div style={{
                    width: "85px", fontSize: "10px", fontFamily: "'JetBrains Mono', monospace",
                    color: "#999", textAlign: "right", flexShrink: 0,
                  }}>{item.name}</div>
                  <div style={{
                    flex: 1, background: "rgba(255,255,255,0.03)", borderRadius: "3px", height: "16px",
                    overflow: "hidden",
                  }}>
                    <div style={{
                      width: `${(item.price / 25) * 100}%`, height: "100%",
                      background: `linear-gradient(90deg, ${item.color}44, ${item.color}88)`,
                      borderRadius: "3px", display: "flex", alignItems: "center",
                      justifyContent: "flex-end", paddingRight: "5px", minWidth: "30px",
                    }}>
                      <span style={{ fontSize: "9px", fontFamily: "'JetBrains Mono', monospace", color: "#fff", fontWeight: 600 }}>
                        ${item.price}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Pricing details */}
            {filtered.map(m => (
              <div key={m.id} style={{
                background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)",
                borderRadius: "12px", padding: "14px 16px",
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "10px" }}>
                  <span style={{ fontSize: "16px" }}>{m.icon}</span>
                  <span style={{ fontWeight: 700, fontSize: "14px", color: m.accent }}>{m.name}</span>
                </div>
                <div style={{
                  display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px", marginBottom: "8px",
                }}>
                  <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: "8px", padding: "10px 12px" }}>
                    <div style={{ fontSize: "10px", color: "#666" }}>輸入</div>
                    <div style={{ fontSize: "18px", fontWeight: 700, color: "#4ADE80", fontFamily: "'JetBrains Mono', monospace" }}>
                      {m.apiPrice.input}
                    </div>
                    <div style={{ fontSize: "9px", color: "#555" }}>/ 1M tokens</div>
                  </div>
                  <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: "8px", padding: "10px 12px" }}>
                    <div style={{ fontSize: "10px", color: "#666" }}>輸出</div>
                    <div style={{ fontSize: "18px", fontWeight: 700, color: "#FB923C", fontFamily: "'JetBrains Mono', monospace" }}>
                      {m.apiPrice.output}
                    </div>
                    <div style={{ fontSize: "9px", color: "#555" }}>/ 1M tokens</div>
                  </div>
                </div>
                <div style={{ fontSize: "11px", color: "#777", lineHeight: 1.5 }}>
                  📌 {m.apiPrice.note}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Features */}
        {activeAspect === "features" && (
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {filtered.map(m => (
              <div key={m.id} style={{
                background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)",
                borderRadius: "12px", padding: "16px",
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "12px" }}>
                  <span style={{ fontSize: "18px" }}>{m.icon}</span>
                  <span style={{ fontWeight: 700, fontSize: "15px", color: m.accent }}>{m.name}</span>
                  <span style={{ fontSize: "11px", color: "#777", fontStyle: "italic" }}>{m.tagline}</span>
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))", gap: "5px", marginBottom: "14px" }}>
                  {m.features.map((f, i) => (
                    <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: "6px", padding: "3px 0" }}>
                      <span style={{ color: m.accent, fontSize: "8px", marginTop: "5px", flexShrink: 0 }}>●</span>
                      <span style={{ fontSize: "12px", color: "#bbb", lineHeight: 1.5 }}>{f}</span>
                    </div>
                  ))}
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px" }}>
                  <div style={{
                    padding: "10px 12px", background: "rgba(74,222,128,0.04)",
                    borderRadius: "8px", border: "1px solid rgba(74,222,128,0.1)",
                  }}>
                    <div style={{ fontSize: "10px", fontWeight: 600, color: "#4ADE80", marginBottom: "4px" }}>✅ 優勢</div>
                    {m.strengths.map((s, i) => (
                      <div key={i} style={{ fontSize: "11px", color: "#8BC8A0", lineHeight: 1.6 }}>· {s}</div>
                    ))}
                  </div>
                  <div style={{
                    padding: "10px 12px", background: "rgba(251,146,60,0.04)",
                    borderRadius: "8px", border: "1px solid rgba(251,146,60,0.1)",
                  }}>
                    <div style={{ fontSize: "10px", fontWeight: 600, color: "#FB923C", marginBottom: "4px" }}>⚠️ 注意</div>
                    {m.weaknesses.map((w, i) => (
                      <div key={i} style={{ fontSize: "11px", color: "#C89860", lineHeight: 1.6 }}>· {w}</div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Audience / Decision */}
        {activeAspect === "audience" && (
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {filtered.map(m => (
              <div key={m.id} style={{
                background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)",
                borderRadius: "12px", padding: "16px",
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "12px" }}>
                  <span style={{ fontSize: "18px" }}>{m.icon}</span>
                  <span style={{ fontWeight: 700, fontSize: "15px", color: m.accent }}>{m.name}</span>
                  <span style={{
                    marginLeft: "auto", fontSize: "11px", fontWeight: 700, color: m.accent,
                    background: `${m.accent}15`, padding: "3px 10px", borderRadius: "6px",
                  }}>{m.verdict}</span>
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: "6px" }}>
                  {m.bestFor.map((b, i) => (
                    <div key={i} style={{
                      padding: "10px 12px", background: `${m.accent}08`,
                      borderRadius: "8px", border: `1px solid ${m.accent}18`,
                      fontSize: "12px", color: "#ccc", lineHeight: 1.4,
                    }}>{b}</div>
                  ))}
                </div>
              </div>
            ))}

            {!selectedModel && (
              <div style={{
                background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)",
                borderRadius: "12px", padding: "18px",
              }}>
                <div style={{ fontSize: "14px", fontWeight: 700, color: "#ddd", marginBottom: "14px" }}>🧭 快速決策指南</div>
                {[
                  { q: "我要最強推理 & 程式碼品質", a: "Claude Opus 4.6", c: "#D97706", why: "推理天花板，Sonnet 4.6 性價比更好" },
                  { q: "我要最便宜的前沿 API", a: "Kimi K2.5", c: "#10B981", why: "$0.60/M 輸入，開源可自部署" },
                  { q: "我要完全開源自部署", a: "Qwen 3.5 / GLM-5", c: "#6366F1", why: "Apache 2.0 / MIT，可完全掌控" },
                  { q: "我是 GitHub 重度工程師", a: "GPT-5.3 Codex", c: "#EF4444", why: "Codex App + GitHub 深度整合最強" },
                  { q: "我想免費試 Agent-First IDE", a: "Antigravity", c: "#3B82F6", why: "預覽期免費，多代理平行調度" },
                  { q: "我需要最低幻覺率", a: "GLM-5", c: "#F59E0B", why: "AA Omniscience Index 業界最佳" },
                  { q: "我做前端開發 & UI 設計", a: "Kimi K2.5", c: "#10B981", why: "UI-to-Code & 視覺除錯特別強" },
                  { q: "我的資料不能離開中國", a: "GLM-5 / Qwen 3.5", c: "#F59E0B", why: "國產晶片推理 + 本地部署" },
                ].map((item, i) => (
                  <div key={i} style={{
                    display: "flex", gap: "10px", padding: "10px 0",
                    borderBottom: i < 7 ? "1px solid rgba(255,255,255,0.03)" : "none",
                    alignItems: "flex-start",
                  }}>
                    <div style={{ fontSize: "11px", color: "#999", flex: 1, lineHeight: 1.5, minWidth: 0 }}>
                      「{item.q}」
                    </div>
                    <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", flexShrink: 0 }}>
                      <span style={{ fontSize: "12px", fontWeight: 700, color: item.c }}>→ {item.a}</span>
                      <span style={{ fontSize: "9px", color: "#666", marginTop: "2px", textAlign: "right" }}>{item.why}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={{
        textAlign: "center", padding: "16px", fontSize: "9px",
        fontFamily: "'JetBrains Mono', monospace", color: "#333",
        borderTop: "1px solid rgba(255,255,255,0.03)",
      }}>
        資料更新：2026 年 2 月 ｜ 價格以各官方公告為準 ｜ 點擊模型卡片可篩選
      </div>
    </div>
  );
}
