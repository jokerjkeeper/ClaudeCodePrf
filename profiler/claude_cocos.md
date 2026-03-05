# claude_cocos.md — Cocos 專案配置 Profile

> 本文件為 Cocos Creator / Cocos 專案的 Claude Code 補充規則，需搭配 `CLAUDE.md` 主文件使用。
> 放置於專案根目錄，與 CLAUDE.md 同級。

---

## 一、專案基礎資訊

```yaml
# ⚠️ 請根據實際專案填寫以下內容
engine: Cocos Creator 3.8         # Cocos Creator 版本 (2.x / 3.x)
render_pipeline: 渲染管线            # builtin / forward-plus / deferred
language: TypeScript              # TypeScript / JavaScript
target_platforms:
  - Android
  - iOS
  - Web
  - WeChat Mini Game
ide: VS Code                       # VS Code / WebStorm
```

---

## 二、Cocos 專案結構約定

```
assets/
├── scripts/               # 腳本目錄
│   ├── core/              # 核心系統（GameManager、EventBus 等）
│   │   ├── game/          # 遊戲管理器
│   │   ├── event/         # 事件系統
│   │   └── ui/            # UI 管理系統
│   ├── ui/                # UI 相關腳本
│   │   ├── components/    # UI 組件
│   │   └── views/          # UI 視圖
│   ├── gameplay/          # 遊戲玩法邏輯
│   │   ├── player/
│   │   ├── enemy/
│   │   └── items/
│   ├── data/              # 數據模型、配置
│   ├── network/           # 網絡相關
│   └── utils/             # 工具類
├── prefabs/               # 預製體
├── scenes/                # 場景文件
├── resources/             # 動態加載資源
├── textures/              # 貼圖資源
├── materials/             # 材質
├── animations/            # 動畫資源
├── audio/                 # 音效、音樂
└── extensions/            # 第三方插件/擴展
```

---

## 三、Log 分析系統

### 3.1 Log 目錄

| 平台 | 路徑 |
|------|------|
| Cocos Creator Editor | 編輯器 Console 面板 |
| Web | 瀏覽器開發者工具 Console |
| Windows | 可使用 Chrome DevTools Protocol |
| Android | `adb logcat -s cocos` 或 `adb logcat -s JS` |
| iOS | Xcode Console |

### 3.2 自動分析規則

> ⚠️ **注意：Cocos Creator Log 處理方式**
> - 瀏覽器開發者工具可導出 Console 內容
> - 原生平台使用 adb 或 Xcode 獲取 log
> - 小程序平台使用開發者工具的 Console 面板

當收到指令分析 log 時，按以下流程執行：

1. **獲取** 從對應平台獲取 log 內容
2. **分類** 所有日誌條目：
   - `Error` → 必須處理，標記為 🔴
   - `Warning` → 評估影響，標記為 🟡
   - `TypeError / ReferenceError` → 最高優先級，標記為 🔴🔴
3. **去重** 相同的錯誤訊息，統計出現次數
4. **生成報告** 保存到 `.claude/reports/report_<date>_<time>.md`

### 3.3 報告格式

```markdown
# Cocos Log 分析報告
## 生成時間: YYYY-MM-DD HH:MM
## Log 來源: <platform>

### 摘要
- 🔴🔴 Exception: X 個
- 🔴 Error: X 個
- 🟡 Warning: X 個

### 嚴重問題（需立即處理）
#### 1. [TypeError] Cannot read property 'xxx' of null
- 出現次數: 15
- 相關腳本: PlayerController.ts:42
- 可能原因: <分析>
- 建議修復: <方案>

### 一般錯誤
...

### 警告（建議處理）
...

### 修復建議優先級
1. <最高優先級問題>
2. <次高優先級問題>
```

### 3.4 基於報告的修復流程

當使用者選擇讓 Claude Code 根據報告修復 bug 時：

1. 讀取報告文件（如 `report_20260305_11_10.md`）
2. 按優先級逐一處理
3. 每修復一個問題，在報告中標記為 `[FIXED]`
4. 修復完成後重新運行分析，確認問題是否解決
5. 更新 session.md

---

## 四、Package 管理

### 4.1 已購買插件參考

所有已購買的付費插件/服務清單維護在 `.claude/references/buyer.md`：

```markdown
# 已購買插件/服務清單

| 插件名稱 | 版本 | Cocos Store 連結 | 用途 | 備註 |
|----------|------|------------------|------|------|
| DragonBones | 5.6.0 | <link> | 骨骼動畫 | 全專案通用 |
| Spine Runtime | 4.1.0 | <link> | Spine 動畫 | 遊戲角色 |
| TiledMap | - | 內建 | 地圖編輯 | 免費內建 |
```

### 4.2 插件使用規則

- **優先使用已購買清單中的插件**，不要引入功能重複的替代品
- 如需新插件，先檢查 `buyer.md` 是否已有類似功能的工具
- 免費插件可直接使用，但需記錄到 `buyer.md`
- **禁止**在代碼中引入未列在清單中的付費插件
- 使用 Cocos Creator 內建的 package 管理系統（package.json）
- 擴展包放在 `extensions/` 目錄下

### 4.3 常用免費/內建功能

在沒有已購買替代品時，優先考慮：

| 功能 | 推薦方案 | 備註 |
|------|----------|------|
| 動畫緩動 | tween.js / cc.tween | Cocos 內建 |
| 狀態管理 | 簡單事件系統 / Redux 模式 | 輕量場景推薦內建 |
| 網絡請求 | cc.loader / XMLHttpRequest | 內建 |
| 對象池 | cc.NodePool | 內建 |
| 粒子效果 | 粒子編輯器 | 內建 |
| 物理引擎 | Box2D (2D) / Bullet (3D) | 內建 |

---

## 五、TypeScript 代碼規範

### 5.1 命名規範

```typescript
// 類名：PascalCase
export class PlayerController extends Component {}

// 類方法：camelCase
public takeDamage(amount: number): void {}

// 私有字段：_camelCase
private _moveSpeed: number = 0;
private _isGrounded: boolean = false;

// 公共屬性：camelCase
public get health(): number { return this._health; }

// 常量：UPPER_SNAKE_CASE
private static readonly MAX_HEALTH: number = 100;

// 接口：I 前綴
export interface IDamageable {}

// 事件：on 前綴
onHealthChange: Event.EventCallback<number> = null;
```

### 5.2 Cocos 特定規範

- **禁止**在 `update()` 中頻繁使用 `find()`、`getComponent()`，應在 `onLoad()` 或 `start()` 中緩存
- **禁止**頻繁使用 `+` 拼接字符串，使用模板字符串或高效方式
- 使用 `@property` 裝飾器暴露屬性到 Inspector，而非 `public` 字段
- 盡量使用 `cc.isValid()` 檢查節點有效性
- 大量生成/銷毀節點時使用 `cc.NodePool`
- 使用 `scheduleOnce` 代替一次性 `setTimeout`
- 事件監聽記得在 `onDestroy()` 中移除

### 5.3 架構模式建議

| 場景 | 推薦模式 |
|------|----------|
| 全局管理器 | Singleton / Director.getDirector() |
| UI 管理 | MVC / 層級管理 |
| 事件通信 | EventTarget / EventBus |
| 狀態機 | State Pattern / 狀態機節點 |
| 數據配置 | 靜態配置類 / JSON 配置 |
| 異步流程 | Promise / async/await |

---

## 六、性能檢查清單

在提交代碼前，確認以下項目：

- [ ] 沒有在 update 中做 GC 分配（new、頻繁對象創建）
- [ ] 沒有未取消訂閱的事件監聽（記得在 onDestroy 中移除）
- [ ] 沒有未釋放的資源引用
- [ ] UI 刷新使用了髒標記模式（dirty flag）而非每幀刷新
- [ ] 物理檢測使用合適的過濾器
- [ ] 大量物件使用了 `cc.NodePool`
- [ ] 沒有同步加載大資源（使用 `resources.load` 或 `assetManager` 異步加載）
- [ ] 紋理使用了合適的壓縮格式
- [ ] 動畫使用了合適的幀率（小平台優化）
- [ ] 避免頻繁的節點查找操作

---

## 七、調試指令

| 命令 | 行為 |
|------|------|
| `/analyze-log <content>` | 分析提供的 log 內容並生成報告 |
| `/fix-report <report_path>` | 根據報告自動修復 bug |
| `/check-perf` | 掃描代碼中的性能問題 |
| `/list-packages` | 列出 package.json 中的依賴 |
| `/check-buyer` | 對比當前插件與 buyer.md，找出未記錄的內容 |
| `/scene-info` | 分析當前場景結構和節點層級 |

---

## 八、Cocos 平台特性注意事項

### 8.1 小程序平台（微信、抖音等）

- **禁止**使用 ES6+ 某些新特性（按平台支持程度）
- 圖片資源大小限制嚴格，注意壓縮
- 音頻需要預加載
- 網絡請求需要域名白名單

### 8.2 Web 平台

- 注意跨域問題（CORS）
- 圖片、音頻資源格式兼容性
- 性能受瀏覽器限制，注意 GC 和幀率

### 8.3 原生平台（Android/iOS）

- 注意內存管理，避免內存洩漏
- 獲取原生權限（相機、存儲等）
- 使用的第三方 SDK 需要原生集成
