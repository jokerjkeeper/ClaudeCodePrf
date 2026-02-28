# ADGC — AI-Domain Game Core 開發規格書

> 供 Claude Code 執行的項目開發規格。基於 ChatGPT 生成的架構文檔，經分析、補強、重組後產出。

---

## 〇、原始文檔分析與改進摘要

### 原始文檔的優點
- 分層架構清晰（Domain / Application / Infrastructure / Adapter）
- 強調 Deterministic 與純邏輯分離，方向正確
- ECS 結構選型合理
- AI 友好設計（Seed 控制、JSON 匯出、批量模擬）思路完整

### 原始文檔的不足與本文檔的改進

| 問題 | 改進 |
|------|------|
| 只有概念描述，缺少具體介面定義 | 補充所有核心 Interface 與類別簽名 |
| ECS 描述過於簡略，未定義 World/Registry | 補充完整 ECS 核心類別設計 |
| Command 模式只有口號，無具體實作路徑 | 定義 ICommand 介面與 CommandBus 流程 |
| Event 設計含糊（「可選 Event Sourcing」） | 明確為必要設計，定義 Event 基類與 EventBus |
| 缺少 DI 容器 / 組裝策略 | 補充 Composition Root 設計 |
| 測試只列了兩行偽代碼 | 補充具體測試結構與命名規範 |
| 無開發任務拆分 | 提供分階段開發任務清單 |
| 缺少錯誤處理策略 | 補充 Result 模式 |

---

## 一、項目總覽

**項目名稱：** AI-Domain Game Core (ADGC)

**目標：** 建立一套純 C# 遊戲核心邏輯框架，滿足：
1. 可在無 Unity 環境下完整運行與測試
2. 邏輯層 100% Deterministic（相同輸入 → 相同輸出）
3. 顯示與邏輯完全解耦
4. 對 AI 友好：可模擬、可重播、可批量運算
5. 可遷移至 Unity / CLI / Server 等不同前端

**語言：** C# (.NET 8+)
**測試框架：** NUnit 或 xUnit
**序列化：** System.Text.Json

---

## 二、架構分層與依賴規則

```
┌─────────────────────────────────────────┐
│  Adapters (Unity / CLI / AISimulator)   │  ← 最外層，可替換
├─────────────────────────────────────────┤
│  Application (UseCases / CommandBus)    │  ← 編排層
├─────────────────────────────────────────┤
│  Domain (ECS + Rules + Events)          │  ← 核心，零外部依賴
├─────────────────────────────────────────┤
│  Infrastructure (Random / Clock / IO)   │  ← 通過介面注入
└─────────────────────────────────────────┘
```

**依賴規則（嚴格執行）：**
- Domain 不引用任何其他層
- Application 只引用 Domain
- Infrastructure 實作 Domain 定義的介面
- Adapter 引用 Application + Infrastructure
- **禁止反向依賴、禁止跨層直接引用**

---

## 三、目錄結構

```
/ADGC.sln
│
├── /src
│   ├── /ADGC.Domain/                    # 核心邏輯（純 C# Class Library）
│   │   ├── /ECS/
│   │   │   ├── Entity.cs
│   │   │   ├── IComponent.cs
│   │   │   ├── World.cs                 # Entity 容器與查詢
│   │   │   └── SystemBase.cs
│   │   ├── /Components/
│   │   │   ├── Position.cs
│   │   │   ├── Health.cs
│   │   │   ├── AttackPower.cs
│   │   │   └── TurnOrder.cs
│   │   ├── /Systems/
│   │   │   ├── MovementSystem.cs
│   │   │   ├── CombatSystem.cs
│   │   │   └── TurnSystem.cs
│   │   ├── /Rules/
│   │   │   └── IRuleValidator.cs
│   │   ├── /Events/
│   │   │   ├── IGameEvent.cs
│   │   │   ├── UnitMoved.cs
│   │   │   ├── DamageApplied.cs
│   │   │   └── TurnEnded.cs
│   │   ├── /Services/                   # Domain 層定義的介面（由 Infrastructure 實作）
│   │   │   ├── IRandomProvider.cs
│   │   │   └── IClock.cs
│   │   ├── GameState.cs
│   │   └── Result.cs                    # 操作結果封裝
│   │
│   ├── /ADGC.Application/              # 應用層（純 C# Class Library）
│   │   ├── /Commands/
│   │   │   ├── ICommand.cs
│   │   │   ├── MoveUnitCommand.cs
│   │   │   ├── AttackCommand.cs
│   │   │   └── EndTurnCommand.cs
│   │   ├── /UseCases/
│   │   │   ├── MoveUnitUseCase.cs
│   │   │   ├── AttackUseCase.cs
│   │   │   └── EndTurnUseCase.cs
│   │   ├── CommandBus.cs
│   │   └── EventBus.cs
│   │
│   ├── /ADGC.Infrastructure/           # 基礎設施（純 C# Class Library）
│   │   ├── SeededRandomProvider.cs
│   │   ├── SystemClock.cs
│   │   └── JsonStateSerializer.cs
│   │
│   └── /ADGC.Adapters/
│       ├── /ADGC.Adapter.CLI/          # Console 前端
│       │   └── Program.cs
│       └── /ADGC.Adapter.AISimulator/  # AI 批量模擬
│           └── Simulator.cs
│
└── /tests
    ├── /ADGC.Domain.Tests/
    │   ├── /Systems/
    │   │   ├── CombatSystemTests.cs
    │   │   └── MovementSystemTests.cs
    │   └── /ECS/
    │       └── WorldTests.cs
    └── /ADGC.Application.Tests/
        └── /UseCases/
            └── MoveUnitUseCaseTests.cs
```

---

## 四、核心介面與類別定義

### 4.1 ECS 核心

```csharp
// === IComponent.cs ===
public interface IComponent { }

// === Entity.cs ===
public sealed class Entity
{
    public int Id { get; }
    private readonly Dictionary<Type, IComponent> _components = new();

    public Entity(int id) => Id = id;

    public void Add<T>(T component) where T : IComponent
        => _components[typeof(T)] = component;

    public T Get<T>() where T : IComponent
        => (T)_components[typeof(T)];

    public bool Has<T>() where T : IComponent
        => _components.ContainsKey(typeof(T));

    public void Remove<T>() where T : IComponent
        => _components.Remove(typeof(T));
}

// === World.cs ===
public sealed class World
{
    private readonly Dictionary<int, Entity> _entities = new();
    private int _nextId = 0;

    public Entity CreateEntity()
    {
        var entity = new Entity(_nextId++);
        _entities[entity.Id] = entity;
        return entity;
    }

    public Entity GetEntity(int id) => _entities[id];

    public IEnumerable<Entity> Query<T>() where T : IComponent
        => _entities.Values.Where(e => e.Has<T>());

    public IEnumerable<Entity> Query<T1, T2>()
        where T1 : IComponent where T2 : IComponent
        => _entities.Values.Where(e => e.Has<T1>() && e.Has<T2>());
}
```

### 4.2 GameState

```csharp
public sealed class GameState
{
    public int TurnNumber { get; set; }
    public int CurrentPlayerId { get; set; }
    public World World { get; set; } = new();
    public List<IGameEvent> PendingEvents { get; set; } = new();

    // 深拷貝，確保 Immutability
    public GameState Clone() { /* Deep copy implementation */ }
}
```

### 4.3 System 基類

```csharp
// 所有 System 遵循純函式風格
public abstract class SystemBase
{
    /// <summary>
    /// 純函式：輸入狀態 + 命令 → 輸出新狀態
    /// </summary>
    public abstract Result<GameState> Execute(GameState state, ICommand command);
}
```

### 4.4 Command / Event

```csharp
// === ICommand.cs ===
public interface ICommand
{
    int PlayerId { get; }
}

// === 範例 Command ===
public record MoveUnitCommand(int PlayerId, int EntityId, int TargetX, int TargetY) : ICommand;
public record AttackCommand(int PlayerId, int AttackerId, int TargetId) : ICommand;
public record EndTurnCommand(int PlayerId) : ICommand;

// === IGameEvent.cs ===
public interface IGameEvent
{
    int TurnNumber { get; }
}

// === 範例 Event ===
public record UnitMoved(int TurnNumber, int EntityId, int FromX, int FromY, int ToX, int ToY) : IGameEvent;
public record DamageApplied(int TurnNumber, int AttackerId, int TargetId, int Damage, int RemainingHp) : IGameEvent;
public record TurnEnded(int TurnNumber, int NextPlayerId) : IGameEvent;
```

### 4.5 Result 模式（錯誤處理）

```csharp
public readonly struct Result<T>
{
    public bool IsSuccess { get; }
    public T Value { get; }
    public string Error { get; }

    private Result(T value) { IsSuccess = true; Value = value; Error = null; }
    private Result(string error) { IsSuccess = false; Value = default; Error = error; }

    public static Result<T> Ok(T value) => new(value);
    public static Result<T> Fail(string error) => new(error);
}
```

### 4.6 Infrastructure 介面

```csharp
public interface IRandomProvider
{
    int Next(int minInclusive, int maxExclusive);
    void SetSeed(int seed);
}

public interface IClock
{
    long GetCurrentTick();
}
```

### 4.7 Application 層 — UseCase 範例

```csharp
public sealed class AttackUseCase
{
    private readonly CombatSystem _combatSystem;
    private readonly EventBus _eventBus;

    public AttackUseCase(CombatSystem combatSystem, EventBus eventBus)
    {
        _combatSystem = combatSystem;
        _eventBus = eventBus;
    }

    public Result<GameState> Execute(GameState state, AttackCommand cmd)
    {
        // 1. 驗證：是否輪到該玩家
        if (state.CurrentPlayerId != cmd.PlayerId)
            return Result<GameState>.Fail("Not your turn");

        // 2. 執行 Domain 邏輯
        var result = _combatSystem.Execute(state, cmd);

        // 3. 發布事件
        if (result.IsSuccess)
        {
            foreach (var evt in result.Value.PendingEvents)
                _eventBus.Publish(evt);
        }

        return result;
    }
}
```

### 4.8 CommandBus

```csharp
public sealed class CommandBus
{
    private readonly Dictionary<Type, Func<GameState, ICommand, Result<GameState>>> _handlers = new();

    public void Register<T>(Func<GameState, T, Result<GameState>> handler) where T : ICommand
    {
        _handlers[typeof(T)] = (state, cmd) => handler(state, (T)cmd);
    }

    public Result<GameState> Dispatch(GameState state, ICommand command)
    {
        if (!_handlers.TryGetValue(command.GetType(), out var handler))
            return Result<GameState>.Fail($"No handler for {command.GetType().Name}");

        return handler(state, command);
    }
}
```

### 4.9 AI Simulator

```csharp
public sealed class Simulator
{
    private readonly CommandBus _commandBus;
    private readonly IRandomProvider _random;

    public SimulationResult RunBatch(int matchCount, int seed)
    {
        var results = new List<MatchResult>();

        for (int i = 0; i < matchCount; i++)
        {
            _random.SetSeed(seed + i);
            var state = CreateInitialState();

            while (!IsGameOver(state))
            {
                var cmd = GenerateAICommand(state);
                var result = _commandBus.Dispatch(state, cmd);
                if (result.IsSuccess) state = result.Value;
            }

            results.Add(new MatchResult(i, GetWinnerId(state), state.TurnNumber));
        }

        return new SimulationResult(results);
    }
}
```

---

## 五、Deterministic 規則（必須嚴格遵守）

1. **所有 System 為純函式**：`f(GameState, ICommand) → Result<GameState>`
2. **禁止全域可變狀態**：不可使用 static mutable fields
3. **隨機數必須通過 `IRandomProvider` 注入**，絕不使用 `System.Random` 直接建構
4. **時間必須通過 `IClock` 注入**，絕不使用 `DateTime.Now`
5. **GameState 修改前必須 Clone**，保證不可變性
6. **禁止 `async/await`** 在 Domain 層中出現
7. **禁止引用** `UnityEngine`、`System.IO`、`System.Net` 等外部命名空間

---

## 六、測試策略

### 命名規範
```
[測試對象]_[場景]_[預期結果]
```
範例：`CombatSystem_AttackWithSufficientDamage_ShouldKillTarget`

### Domain 測試（100% 核心規則覆蓋）

```csharp
[Test]
public void CombatSystem_Attack_ShouldReduceTargetHealth()
{
    // Arrange
    var state = CreateStateWithTwoUnits(attackPower: 10, targetHp: 100);
    var cmd = new AttackCommand(PlayerId: 0, AttackerId: 0, TargetId: 1);
    var system = new CombatSystem(new SeededRandomProvider(seed: 42));

    // Act
    var result = system.Execute(state, cmd);

    // Assert
    Assert.IsTrue(result.IsSuccess);
    var targetHp = result.Value.World.GetEntity(1).Get<Health>().Current;
    Assert.AreEqual(90, targetHp);
}
```

### 模擬測試

```csharp
[Test]
public void Simulation_10000Matches_WinRateShouldBeBalanced()
{
    var simulator = CreateSimulator();
    var result = simulator.RunBatch(matchCount: 10000, seed: 12345);

    var winRate = result.GetWinRate(playerId: 0);
    Assert.That(winRate, Is.InRange(0.45, 0.55));
}
```

### Replay 測試（Deterministic 驗證）

```csharp
[Test]
public void Replay_SameSeed_ShouldProduceIdenticalResult()
{
    var result1 = RunMatch(seed: 42);
    var result2 = RunMatch(seed: 42);

    Assert.AreEqual(
        JsonSerializer.Serialize(result1),
        JsonSerializer.Serialize(result2)
    );
}
```

---

## 七、開發階段任務清單

按以下順序開發，**嚴禁跳過或反向依賴**：

### Phase 1：Domain 核心（估計 2-3 天）
- [ ] 建立 Solution 與 Project 結構
- [ ] 實作 ECS 核心：`Entity`、`IComponent`、`World`
- [ ] 實作基礎 Component：`Position`、`Health`、`AttackPower`
- [ ] 實作 `IGameEvent` 與基礎事件
- [ ] 實作 `GameState` 與 `Clone()`
- [ ] 實作 `Result<T>`
- [ ] 定義 `IRandomProvider`、`IClock` 介面
- [ ] 實作 `MovementSystem`、`CombatSystem`、`TurnSystem`
- [ ] **撰寫所有 Domain 單元測試**

### Phase 2：Application 層（估計 1-2 天）
- [ ] 實作 `ICommand` 與所有 Command
- [ ] 實作 `CommandBus`
- [ ] 實作 `EventBus`
- [ ] 實作所有 UseCase
- [ ] **撰寫 Application 層測試**

### Phase 3：Infrastructure（估計 1 天）
- [ ] 實作 `SeededRandomProvider`
- [ ] 實作 `SystemClock`
- [ ] 實作 `JsonStateSerializer`

### Phase 4：Adapters（估計 1-2 天）
- [ ] 實作 CLI Adapter（Console 互動）
- [ ] 實作 AI Simulator（批量模擬）
- [ ] 驗證端到端流程

### Phase 5：整合驗證
- [ ] Replay Deterministic 測試通過
- [ ] 10000 場批量模擬正常運行
- [ ] JSON State 匯出 / 匯入驗證
- [ ] 確認 Domain 專案無任何外部依賴引用

---

## 八、Claude Code 執行指引

### 開發原則
1. **先寫測試，再寫實作**（TDD 優先）
2. 每完成一個 Phase 跑一次全部測試
3. 確保 Domain 專案的 .csproj 不引用任何外部套件
4. 使用 `dotnet test` 驗證

### 代碼風格
- 使用 C# 12 語法（record、pattern matching）
- 所有公開 API 加 XML Doc Comment
- 一個檔案一個類別
- 命名空間對應目錄結構：`ADGC.Domain.ECS`、`ADGC.Application.Commands` 等

### 品質檢查
- `dotnet build --warnaserror` 無警告
- `dotnet test` 全部通過
- Domain 層零外部依賴（可用 `dotnet list package` 驗證）

---

## 九、未來擴展方向（本階段不實作）

- Unity Adapter（MonoBehaviour 綁定 + 動畫映射）
- Server Adapter（WebSocket / gRPC）
- AI 訓練介面（State → Feature Vector 轉換）
- Event Sourcing 持久化（事件流存儲與重建）
- 插件系統（動態載入遊戲規則模組）
