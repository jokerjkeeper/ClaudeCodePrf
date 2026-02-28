# claude_unity.md — Unity 專案配置 Profile

> 本文件為 Unity 專案的 Claude Code 補充規則，需搭配 `CLAUDE.md` 主文件使用。
> 放置於專案根目錄，與 CLAUDE.md 同級。

---

## 一、專案基礎資訊

```yaml
# ⚠️ 請根據實際專案填寫以下內容
engine: Unity 2022.3 LTS        # Unity 版本
render_pipeline: URP             # URP / HDRP / Built-in
scripting_backend: IL2CPP        # IL2CPP / Mono
target_platforms:
  - Android
  - iOS
  - Windows
code_language: C#
ide: Rider                       # Rider / VS Code / Visual Studio
```

---

## 二、Unity 專案結構約定

```
Assets/
├── _Project/              # 專案核心代碼（不要放在 Assets 根目錄散落）
│   ├── Scripts/
│   │   ├── Core/          # 核心系統（GameManager、EventBus 等）
│   │   ├── UI/            # UI 相關腳本
│   │   ├── Gameplay/      # 遊戲玩法邏輯
│   │   ├── Data/          # 數據模型、ScriptableObject
│   │   ├── Network/       # 網絡相關
│   │   └── Utils/         # 工具類
│   ├── Prefabs/
│   ├── Scenes/
│   ├── Materials/
│   ├── Animations/
│   └── Resources/         # 僅放需要動態加載的資源
├── Plugins/               # 第三方插件
├── StreamingAssets/        # 需要原樣打包的資源
└── Editor/                # Editor 擴展腳本
```

---

## 三、Log 分析系統

### 3.1 Log 目錄

| 平台 | 路徑 |
|------|------|
| Windows Editor | `%LOCALAPPDATA%/Unity/Editor/Editor.log` |
| Windows Player | `%APPDATA%/../LocalLow/<CompanyName>/<ProductName>/Player.log` |
| macOS Editor | `~/Library/Logs/Unity/Editor.log` |
| Android | `adb logcat -s Unity` |

### 3.2 自動分析規則

當收到指令分析 log 時，按以下流程執行：

1. **讀取** 指定的 log 文件
2. **分類** 所有日誌條目：
   - `ERROR` → 必須處理，標記為 🔴
   - `WARNING` → 評估影響，標記為 🟡
   - `EXCEPTION` → 最高優先級，標記為 🔴🔴
3. **去重** 相同的錯誤訊息，統計出現次數
4. **生成報告** 保存到 `.claude/reports/report_<date>_<time>.md`

### 3.3 報告格式

```markdown
# Unity Log 分析報告
## 生成時間: YYYY-MM-DD HH:MM
## Log 來源: <file_path>

### 摘要
- 🔴🔴 Exception: X 個
- 🔴 Error: X 個
- 🟡 Warning: X 個

### 嚴重問題（需立即處理）
#### 1. [Exception] NullReferenceException
- 出現次數: 15
- 首次出現: 行號 XXX
- 相關腳本: PlayerController.cs:42
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

1. 讀取報告文件（如 `report_20260205_11_10.md`）
2. 按優先級逐一處理
3. 每修復一個問題，在報告中標記為 `[FIXED]`
4. 修復完成後重新運行分析，確認問題是否解決
5. 更新 session.md

---

## 四、Package 管理

### 4.1 已購買插件參考

所有已購買的付費插件清單維護在 `.claude/references/buyer.md`：

```markdown
# 已購買插件清單

| 插件名稱 | 版本 | Asset Store 連結 | 用途 | 備註 |
|----------|------|------------------|------|------|
| DOTween Pro | 1.2.7 | <link> | 動畫緩動 | 全專案通用 |
| Odin Inspector | 3.3.1 | <link> | Editor 擴展 | 僅 Editor |
| UniTask | 2.5.0 | <link> | 異步處理 | 免費，推薦使用 |
```

### 4.2 插件使用規則

- **優先使用已購買清單中的插件**，不要引入功能重複的替代品
- 如需新插件，先檢查 `buyer.md` 是否已有類似功能的工具
- 免費插件可直接使用，但需記錄到 `buyer.md`
- **禁止**在代碼中引入未列在清單中的付費插件
- 使用 Unity Package Manager (UPM) 管理的插件優先於手動匯入

### 4.3 常用免費推薦插件

在沒有已購買替代品時，優先考慮：

| 功能 | 推薦插件 | 備註 |
|------|----------|------|
| 異步 | UniTask | 替代原生 Coroutine |
| 依賴注入 | VContainer | 輕量 DI 框架 |
| 響應式 | UniRx / R3 | 事件驅動架構 |
| 序列化 | Newtonsoft JSON | Unity 官方支持 |
| 對象池 | Unity 內建 ObjectPool | 2021+ 內建 |

---

## 五、C# 代碼規範

### 5.1 命名規範

```csharp
// 類名、方法名：PascalCase
public class PlayerController : MonoBehaviour { }
public void TakeDamage(float amount) { }

// 私有字段：_camelCase
private float _moveSpeed;
private bool _isGrounded;

// 公共屬性：PascalCase
public float Health { get; private set; }

// 常量：UPPER_SNAKE_CASE
private const int MAX_HEALTH = 100;

// 接口：I 前綴
public interface IDamageable { }

// 事件：On 前綴
public event Action<float> OnHealthChanged;
```

### 5.2 Unity 特定規範

- **禁止**在 `Update()` 中使用 `Find()`、`GetComponent()`，應在 `Awake()` 或 `Start()` 中緩存
- **禁止**頻繁使用 `string` 拼接，使用 `StringBuilder` 或 `string.Format()`
- 使用 `[SerializeField]` 而非 `public` 字段暴露到 Inspector
- 使用 `TryGetComponent()` 替代 `GetComponent()` + null 檢查
- 盡量使用 `CompareTag()` 替代 `tag ==`
- 大量生成/銷毀物件時使用對象池模式

### 5.3 架構模式建議

| 場景 | 推薦模式 |
|------|----------|
| 全局管理器 | Singleton + ServiceLocator |
| UI 管理 | MVC / MVP |
| 事件通信 | EventBus / Observer |
| 狀態機 | State Pattern |
| 數據配置 | ScriptableObject |
| 異步流程 | UniTask + async/await |

---

## 六、性能檢查清單

在提交代碼前，確認以下項目：

- [ ] 沒有在 Update 中做 GC 分配（new、LINQ、string 拼接）
- [ ] 沒有未取消訂閱的事件監聽
- [ ] 沒有未釋放的資源引用
- [ ] UI 刷新使用了髒標記模式（dirty flag）而非每幀刷新
- [ ] 物理檢測使用了 NonAlloc 版本（RaycastNonAlloc 等）
- [ ] 大量物件使用了對象池
- [ ] 沒有同步加載大資源（使用 Addressables 或異步加載）

---

## 七、調試指令

| 命令 | 行為 |
|------|------|
| `/analyze-log <path>` | 分析指定 log 文件並生成報告 |
| `/fix-report <report_path>` | 根據報告自動修復 bug |
| `/check-perf` | 掃描代碼中的性能問題 |
| `/list-packages` | 列出當前已安裝的所有 package |
| `/check-buyer` | 對比已安裝插件與 buyer.md，找出未記錄的插件 |
