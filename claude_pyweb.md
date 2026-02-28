# claude_pyweb.md — Python Web 專案配置 Profile

> 本文件為 Python Web 專案的 Claude Code 補充規則，需搭配 `CLAUDE.md` 主文件使用。
> 放置於專案根目錄，與 CLAUDE.md 同級。

---

## 一、專案基礎資訊

```yaml
# ⚠️ 請根據實際專案填寫以下內容
framework: FastAPI                # FastAPI / Django / Flask
python_version: "3.12"
frontend: React + Vite            # React / Vue / Next.js / Jinja2 / 無（純 API）
css_framework: Tailwind CSS 3     # Tailwind / Bootstrap / MUI
database: PostgreSQL 16           # PostgreSQL / MySQL / SQLite
orm: SQLAlchemy 2.0               # SQLAlchemy / Django ORM / Tortoise ORM
cache: Redis                      # Redis / Memcached / none
task_queue: Celery + Redis        # Celery / Dramatiq / ARQ / none
package_manager: uv               # uv / poetry / pip
deployment: Docker                # Docker / Gunicorn / Uvicorn 直接部署
```

---

## 二、資料庫配置

### 2.1 支持的資料庫預設

#### SQLite（開發環境 / 小型專案）

```python
# FastAPI + SQLAlchemy
DATABASE_URL = "sqlite+aiosqlite:///./app.db"

# Django
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

#### PostgreSQL（生產環境推薦）

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/app_db
# Django 格式
DB_ENGINE=django.db.backends.postgresql
DB_NAME=app_db
DB_USER=app_user
DB_PASSWORD=           # 環境變數注入
DB_HOST=127.0.0.1
DB_PORT=5432
```

#### MySQL

```env
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/app_db?charset=utf8mb4
```

#### Redis

```env
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_URL=redis://localhost:6379/1
REDIS_CELERY_URL=redis://localhost:6379/2
```

### 2.2 資料庫規範

- 表名使用複數形式的 `snake_case`
- 所有 model 必須包含 `id`、`created_at`、`updated_at` 欄位
- 使用 Alembic（FastAPI）或 Django migrations 管理 schema 變更
- Migration 必須可回滾
- 複雜查詢封裝到 Repository 或 Manager 層
- 禁止在業務代碼中寫原始 SQL，除非 ORM 無法表達

---

## 三、帳戶角色管理系統

### 3.1 預設角色架構

```python
from enum import Enum

class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"    # 超級管理員 — 系統最高權限
    ADMIN       = "admin"          # 管理員 — 後台全部功能
    SALES       = "sales"          # 銷售 — 客戶管理、訂單、報表
    AGENT       = "agent"          # 代理 — 下級會員管理、佣金
    OPERATOR    = "operator"       # 運維 — 系統監控、日誌、配置
    MEMBER      = "member"         # 會員 — 前台基本功能
```

### 3.2 權限模型

```python
# 建議使用 RBAC 模型（Role-Based Access Control）

# permissions 表
class Permission(Base):
    __tablename__ = "permissions"
    id: int
    group: str          # "user", "order", "report", "system", "content"
    code: str           # "user.list", "user.create", ...
    name: str           # 人類可讀名稱

# role_permissions 關聯表
class RolePermission(Base):
    __tablename__ = "role_permissions"
    role_id: int
    permission_id: int

# 權限分組
PERMISSION_GROUPS = {
    "user":    ["user.list", "user.create", "user.edit", "user.delete", "user.export"],
    "order":   ["order.list", "order.create", "order.edit", "order.cancel", "order.refund"],
    "report":  ["report.view", "report.export", "report.financial"],
    "system":  ["system.config", "system.log", "system.cache", "system.backup"],
    "content": ["content.list", "content.create", "content.edit", "content.publish"],
}
```

### 3.3 權限裝飾器（FastAPI 範例）

```python
from functools import wraps

def require_permission(*permissions: str):
    """路由權限裝飾器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if not current_user.has_any_permission(permissions):
                raise HTTPException(status_code=403, detail="權限不足")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# 使用方式
@router.get("/users")
@require_permission("user.list")
async def list_users(current_user: User = Depends(get_current_user)):
    ...
```

### 3.4 後台模塊與角色映射

| 模塊 | 功能 | 可訪問角色 |
|------|------|-----------|
| 儀表板 | 數據概覽、圖表 | 全部管理角色 |
| 用戶管理 | CRUD、角色分配 | super_admin, admin |
| 訂單管理 | 查看、處理、退款 | admin, sales |
| 代理管理 | 審核、佣金設定 | admin, agent |
| 內容管理 | 文章、公告 | admin, operator |
| 財務報表 | 收入統計、導出 | super_admin, admin |
| 系統設定 | 站點配置 | super_admin, operator |
| 操作日誌 | 全部記錄 | super_admin, operator |

---

## 四、三端響應式設計

### 4.1 斷點定義（與 PHP profile 統一）

| 端 | 斷點範圍 | 佈局策略 |
|----|----------|----------|
| 手機端 | < 768px | 單列、底部導航、漢堡選單、觸控友善（44px 最小點擊區域） |
| 平板端 | 768px - 1024px | 雙列、側邊欄可收合 |
| 桌面端 | > 1024px | 多列、固定側邊欄 |

### 4.2 前後端分離時的規範

- 前端獨立 repo 或 `frontend/` 子目錄
- API 統一加 `/api/v1/` 前綴
- 開發環境使用 proxy 解決跨域，生產環境由 Nginx 處理
- 前端靜態資源由 CDN 或 Nginx 提供，不經過 Python 服務

---

## 五、專案結構

### 5.1 FastAPI 專案結構

```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI 入口
│   ├── config.py              # 配置管理（pydantic-settings）
│   ├── database.py            # 資料庫連接
│   ├── dependencies.py        # 全局依賴
│   ├── api/                   # 路由層
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py      # v1 路由匯總
│   │   │   ├── users.py
│   │   │   ├── orders.py
│   │   │   └── auth.py
│   │   └── admin/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── users.py
│   │       └── system.py
│   ├── services/              # 業務邏輯層
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── order_service.py
│   ├── repositories/          # 數據訪問層
│   │   ├── __init__.py
│   │   ├── user_repo.py
│   │   └── order_repo.py
│   ├── models/                # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── order.py
│   ├── schemas/               # Pydantic 輸入/輸出 schema
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── order.py
│   ├── core/                  # 核心功能
│   │   ├── security.py        # JWT、密碼加密
│   │   ├── permissions.py     # RBAC 權限系統
│   │   └── exceptions.py      # 自定義異常
│   └── utils/                 # 工具函數
│       ├── pagination.py
│       └── logger.py
├── alembic/                   # 資料庫 migration
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   └── test_orders.py
├── frontend/                  # 前端專案（如使用前後端分離）
├── alembic.ini
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

### 5.2 Django 專案結構

```
project-root/
├── config/                    # 專案配置（替代預設的 project_name/）
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/              # 帳戶系統
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── services.py        # 業務邏輯不寫在 views 裡
│   │   └── permissions.py
│   ├── orders/
│   └── dashboard/
├── common/                    # 共用模塊
│   ├── mixins.py
│   ├── pagination.py
│   └── exceptions.py
├── templates/                 # 如使用 Django Template
├── static/
├── manage.py
├── pyproject.toml
└── docker-compose.yml
```

---

## 六、Python 代碼規範

### 6.1 命名規範

```python
# 類名：PascalCase
class UserService:
    pass

# 函數/方法：snake_case
def get_user_by_id(user_id: int) -> User:
    pass

# 變數：snake_case
user_email = request.email

# 常量：UPPER_SNAKE_CASE
MAX_LOGIN_ATTEMPTS = 5

# 私有方法/屬性：_前綴
def _validate_token(self, token: str) -> bool:
    pass

# 模塊名：snake_case
# user_service.py, order_repo.py
```

### 6.2 類型標注

- **所有**函數參數和返回值必須有類型標注
- 使用 `Pydantic` 定義 API 的輸入/輸出 schema
- 複雜類型使用 `TypeAlias` 或 `TypeVar`

```python
from typing import Optional

async def get_user(user_id: int) -> Optional[UserResponse]:
    ...

# Pydantic schema
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
```

### 6.3 必須遵守的規則

- 路由函數（view/endpoint）中**禁止**直接寫業務邏輯，必須調用 Service
- 所有外部調用（DB、HTTP、文件）使用 `async`
- 異常使用自定義 Exception 類，不直接 raise 通用 Exception
- 使用 `logging` 模塊，禁止使用 `print()` 做日誌
- 環境變數使用 `pydantic-settings` 或 `python-dotenv` 管理
- 禁止 `import *`

---

## 七、API 規範

### 7.1 統一響應格式

```python
# schemas/response.py
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None

class PaginatedData(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    per_page: int
    pages: int

# 使用方式
@router.get("/users", response_model=ApiResponse[PaginatedData[UserResponse]])
async def list_users(page: int = 1, per_page: int = 20):
    ...
```

### 7.2 錯誤響應

```python
# core/exceptions.py
class AppException(Exception):
    def __init__(self, code: int, message: str, errors: dict | None = None):
        self.code = code
        self.message = message
        self.errors = errors

# 全局異常處理器
@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "message": exc.message, "errors": exc.errors}
    )
```

---

## 八、安全規範

- 密碼使用 `bcrypt`（推薦 `passlib`）加密
- API 認證使用 JWT（`python-jose`）或 OAuth2
- 所有用戶輸入通過 Pydantic schema 驗證
- SQL 查詢僅通過 ORM，禁止原始 SQL 拼接
- CORS 在生產環境限制具體域名，不使用 `*`
- 敏感配置僅通過 `.env` 注入
- 文件上傳驗證類型、大小，存儲在隔離目錄
- Rate limiting 使用 `slowapi` 或中間件實現

---

## 九、測試規範

```python
# 使用 pytest + httpx (FastAPI) 或 pytest-django

# 測試文件命名：test_<module>.py
# 測試函數命名：test_<行為描述>

# FastAPI 範例
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_success(client: AsyncClient, db_session):
    response = await client.post("/api/v1/users", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "securepass123"
    })
    assert response.status_code == 200
    assert response.json()["data"]["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient, db_session):
    # 先創建一個用戶
    # 再用相同 email 創建，預期 409
    ...
```

---

## 十、專案指令

| 命令 | 行為 |
|------|------|
| `/init-fastapi` | 生成 FastAPI 專案骨架（含完整目錄結構、配置、DB 連接） |
| `/init-django` | 生成 Django 專案骨架 |
| `/init-auth` | 生成 JWT 認證 + RBAC 權限系統完整代碼 |
| `/init-admin` | 生成後台管理 API 框架 |
| `/db-setup <type>` | 按指定類型生成資料庫配置與連接代碼 |
| `/make-crud <model>` | 為指定模型生成完整 CRUD（router、service、repo、schema、test） |
| `/make-migration <desc>` | 創建新的 Alembic migration |
| `/check-security` | 掃描安全問題（SQL 注入、硬編碼密碼、CORS 配置等） |
| `/check-types` | 執行 mypy 類型檢查並報告問題 |
| `/api-doc` | 根據路由和 schema 生成 API 文檔（FastAPI 自帶 /docs） |
