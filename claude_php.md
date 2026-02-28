# claude_php.md — PHP Web 專案配置 Profile

> 本文件為 PHP Web 專案的 Claude Code 補充規則，需搭配 `CLAUDE.md` 主文件使用。
> 放置於專案根目錄，與 CLAUDE.md 同級。

---

## 一、專案基礎資訊

```yaml
# ⚠️ 請根據實際專案填寫以下內容
framework: Laravel 11             # Laravel / ThinkPHP / CodeIgniter / 原生
php_version: 8.3
frontend: Vue 3 + Vite            # Vue / React / Blade / Livewire
css_framework: Tailwind CSS 3     # Tailwind / Bootstrap
database: MySQL 8.0               # MySQL / PostgreSQL / MariaDB
cache: Redis                      # Redis / Memcached / File
queue: Redis                      # Redis / RabbitMQ / Database
search_engine: none               # Elasticsearch / Meilisearch / none
deployment: Docker                # Docker / 寶塔 / 手動部署
```

---

## 二、資料庫配置

### 2.1 支持的資料庫預設

根據專案需求選擇，以下為快速配置模板：

#### SQLite（輕量 / 開發環境）

```env
DB_CONNECTION=sqlite
DB_DATABASE=/path/to/database.sqlite
```

適用場景：原型開發、小型專案、單機部署。

#### MySQL（生產環境推薦）

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=app_db
DB_USERNAME=app_user
DB_PASSWORD=          # 從環境變數注入，禁止 hardcode
DB_CHARSET=utf8mb4
DB_COLLATION=utf8mb4_unicode_ci
```

#### Redis（緩存 / 隊列 / Session）

```env
REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379
REDIS_DB=0            # 主業務
REDIS_CACHE_DB=1      # 緩存
REDIS_SESSION_DB=2    # Session
```

### 2.2 資料庫規範

- 表名使用複數形式的 `snake_case`（如 `user_roles`）
- 主鍵統一使用 `id`（自增 bigint 或 UUID）
- 時間欄位統一使用 `created_at`、`updated_at`、`deleted_at`（軟刪除）
- 索引命名：`idx_<table>_<columns>`
- 外鍵命名：`fk_<table>_<ref_table>_<column>`
- Migration 文件必須包含 `up()` 和 `down()`
- 禁止在 migration 中使用原始 SQL，除非不可避免

---

## 三、帳戶角色管理系統

### 3.1 預設角色架構

當啟用帳戶管理系統時，使用以下標準角色模型：

```
┌─────────────────────────────────────────────────────┐
│                   super_admin                        │
│              （超級管理員，最高權限）                    │
├──────────┬──────────┬──────────┬────────────────────┤
│  admin   │  sales   │  agent   │     operator       │
│  管理員   │  銷售    │  代理    │      運維           │
├──────────┴──────────┴──────────┴────────────────────┤
│                     member                           │
│                  （普通會員）                          │
└─────────────────────────────────────────────────────┘
```

### 3.2 權限表結構

```php
// 建議使用 spatie/laravel-permission 套件

// 角色定義
$roles = [
    'super_admin' => '超級管理員 — 系統最高權限',
    'admin'       => '管理員 — 管理後台全部功能',
    'sales'       => '銷售 — 客戶管理、訂單查看、報表',
    'agent'       => '代理 — 下級會員管理、佣金查看',
    'operator'    => '運維 — 系統監控、日誌查看、配置管理',
    'member'      => '會員 — 前台基本功能',
];

// 權限分組
$permission_groups = [
    'user'    => ['user.list', 'user.create', 'user.edit', 'user.delete', 'user.export'],
    'order'   => ['order.list', 'order.create', 'order.edit', 'order.cancel', 'order.refund'],
    'report'  => ['report.view', 'report.export', 'report.financial'],
    'system'  => ['system.config', 'system.log', 'system.cache', 'system.backup'],
    'content' => ['content.list', 'content.create', 'content.edit', 'content.publish'],
];
```

### 3.3 後台管理介面功能清單

| 模塊 | 功能 | 可訪問角色 |
|------|------|-----------|
| 儀表板 | 數據概覽、圖表 | 全部管理角色 |
| 用戶管理 | CRUD、角色分配、停用 | super_admin, admin |
| 訂單管理 | 查看、處理、退款 | admin, sales |
| 代理管理 | 代理審核、佣金設定 | admin, agent |
| 內容管理 | 文章、公告、Banner | admin, operator |
| 財務報表 | 收入統計、導出 | super_admin, admin |
| 系統設定 | 站點配置、參數 | super_admin, operator |
| 操作日誌 | 全部操作記錄 | super_admin, operator |

---

## 四、三端響應式設計

### 4.1 斷點定義

```css
/* Tailwind 預設斷點，專案統一使用 */
/* sm:  640px  — 手機橫屏 */
/* md:  768px  — 平板 */
/* lg:  1024px — 小型筆電 */
/* xl:  1280px — 桌面 */
/* 2xl: 1536px — 大屏 */
```

### 4.2 三端適配策略

| 端 | 斷點範圍 | 佈局策略 |
|----|----------|----------|
| 手機端 | < 768px | 單列佈局、底部導航、漢堡選單、觸控友善（最小點擊區域 44px） |
| 平板端 | 768px - 1024px | 雙列佈局、側邊欄可收合、適度留白 |
| 桌面端 | > 1024px | 多列佈局、固定側邊欄、完整功能展示 |

### 4.3 Mobile First 規範

- 所有 CSS 以手機端為基礎，向上覆蓋（mobile-first）
- 圖片使用 `<picture>` 或 `srcset` 提供多尺寸
- 表格在手機端轉為卡片式展示或橫向滾動
- 表單在手機端垂直堆疊，每個輸入框佔滿寬度
- 導航在手機端使用底部 Tab Bar 或漢堡選單

---

## 五、PHP / Laravel 代碼規範

### 5.1 命名規範

```php
// 類名：PascalCase
class UserController extends Controller {}
class OrderService {}

// 方法名：camelCase
public function getUserById(int $id) {}

// 變數名：camelCase
$userEmail = $request->input('email');

// 常量：UPPER_SNAKE_CASE
const MAX_LOGIN_ATTEMPTS = 5;

// 路由名：dot.notation
Route::name('admin.users.index');

// 配置鍵：dot.notation + snake_case
config('app.admin_email');

// 資料庫欄位：snake_case
$table->string('first_name');
```

### 5.2 架構分層

```
app/
├── Http/
│   ├── Controllers/       # 控制器 — 僅處理請求/響應，不寫業務邏輯
│   ├── Middleware/         # 中間件
│   ├── Requests/          # 表單驗證 — 所有驗證必須放在 FormRequest
│   └── Resources/         # API Resource 轉換
├── Services/              # 業務邏輯層 — 核心邏輯全部在此
├── Repositories/          # 數據訪問層 — 複雜查詢封裝（可選）
├── Models/                # Eloquent 模型
├── Events/                # 事件
├── Listeners/             # 事件監聽
├── Jobs/                  # 隊列任務
├── Notifications/         # 通知
└── Enums/                 # 枚舉類（PHP 8.1+）
```

### 5.3 必須遵守的規則

- Controller 中**禁止**直接寫業務邏輯，必須調用 Service
- 所有請求參數使用 `FormRequest` 驗證，Controller 中不出現 `$request->validate()`
- 數據返回統一使用 `API Resource`，不在 Controller 中手動組裝 JSON
- 使用 `Enum` 替代魔法數字和字串常量
- 隊列任務必須實現 `ShouldQueue` 接口
- 敏感操作必須記錄到操作日誌

---

## 六、API 規範

### 6.1 統一響應格式

```json
// 成功
{
  "code": 200,
  "message": "success",
  "data": { ... }
}

// 分頁
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [ ... ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total": 150,
      "last_page": 8
    }
  }
}

// 錯誤
{
  "code": 422,
  "message": "驗證失敗",
  "errors": {
    "email": ["郵箱格式不正確"]
  }
}
```

### 6.2 RESTful 路由規範

```php
// 後台 API
Route::prefix('admin')->middleware(['auth', 'role:admin'])->group(function () {
    Route::apiResource('users', Admin\UserController::class);
    Route::apiResource('orders', Admin\OrderController::class);
});

// 前台 API
Route::prefix('api/v1')->middleware('auth:sanctum')->group(function () {
    Route::get('profile', [ProfileController::class, 'show']);
    Route::put('profile', [ProfileController::class, 'update']);
});
```

---

## 七、安全規範

- 所有使用者輸入必須驗證和過濾
- SQL 查詢僅使用 Eloquent 或 Query Builder，**禁止**原始 SQL 拼接
- 密碼使用 `bcrypt` 或 `argon2` 加密
- API 認證使用 Laravel Sanctum 或 Passport
- CSRF 保護不可關閉（API 路由除外）
- 敏感配置使用 `.env`，禁止提交到 Git
- 文件上傳必須驗證類型和大小，存儲在非公開目錄

---

## 八、專案指令

| 命令 | 行為 |
|------|------|
| `/init-auth` | 生成帳戶角色管理系統的完整腳手架（migration、model、controller、route） |
| `/init-admin` | 生成後台管理介面基礎框架 |
| `/db-setup <type>` | 按指定類型（mysql/sqlite/redis）生成資料庫配置 |
| `/make-crud <model>` | 為指定模型生成完整 CRUD（controller、service、request、resource、route） |
| `/check-security` | 掃描代碼中的安全問題 |
| `/api-doc` | 根據路由和 FormRequest 自動生成 API 文檔 |
