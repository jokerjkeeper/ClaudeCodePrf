# claude_vue.md — Vue 專案配置 Profile

> 本文件為 Vue 前端專案的 Claude Code 補充規則，需搭配 `CLAUDE.md` 主文件使用。
> 放置於專案根目錄，與 CLAUDE.md 同級。

---

## 一、專案基礎資訊

```yaml
# ⚠️ 請根據實際專案填寫以下內容
framework: Vue 3                  # Vue 3 (Composition API)
build_tool: Vite 6                # Vite / Webpack / Nuxt
language: TypeScript              # TypeScript / JavaScript
css_framework: Tailwind CSS 4     # Tailwind / UnoCSS / Element Plus / Vuetify
state_management: Pinia           # Pinia / Vuex（僅維護舊專案）
router: Vue Router 4              # Vue Router
http_client: Axios                # Axios / ofetch / ky
package_manager: pnpm             # pnpm / npm / yarn / bun
testing: Vitest + Vue Test Utils  # Vitest / Jest
e2e_testing: Playwright           # Playwright / Cypress
deployment: Docker + Nginx        # Docker / Vercel / Netlify / Nginx
```

---

## 二、專案結構

### 2.1 標準 Vue 3 專案結構

```
project-root/
├── src/
│   ├── main.ts                   # 應用入口
│   ├── App.vue                   # 根組件
│   ├── router/                   # 路由配置
│   │   ├── index.ts
│   │   ├── routes.ts             # 路由定義（可按模塊拆分）
│   │   └── guards.ts             # 路由守衛
│   ├── stores/                   # Pinia 狀態管理
│   │   ├── index.ts
│   │   ├── user.ts
│   │   └── app.ts
│   ├── views/                    # 頁面級組件（對應路由）
│   │   ├── home/
│   │   │   └── HomeView.vue
│   │   ├── auth/
│   │   │   ├── LoginView.vue
│   │   │   └── RegisterView.vue
│   │   └── dashboard/
│   │       └── DashboardView.vue
│   ├── components/               # 可復用組件
│   │   ├── common/               # 通用基礎組件
│   │   │   ├── AppButton.vue
│   │   │   ├── AppModal.vue
│   │   │   └── AppTable.vue
│   │   ├── layout/               # 佈局組件
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppSidebar.vue
│   │   │   └── AppFooter.vue
│   │   └── business/             # 業務組件
│   │       └── UserCard.vue
│   ├── composables/              # 組合式函數（Composition API 邏輯復用）
│   │   ├── useAuth.ts
│   │   ├── usePagination.ts
│   │   └── useTheme.ts
│   ├── api/                      # API 請求層
│   │   ├── index.ts              # Axios 實例與攔截器
│   │   ├── user.ts
│   │   └── order.ts
│   ├── types/                    # TypeScript 類型定義
│   │   ├── api.d.ts
│   │   ├── user.d.ts
│   │   └── global.d.ts
│   ├── utils/                    # 工具函數
│   │   ├── format.ts
│   │   ├── storage.ts
│   │   └── validate.ts
│   ├── assets/                   # 靜態資源
│   │   ├── images/
│   │   └── styles/
│   │       ├── main.css
│   │       └── variables.css
│   └── constants/                # 常量定義
│       └── index.ts
├── public/                       # 靜態公共資源
├── tests/
│   ├── unit/                     # 單元測試
│   └── e2e/                      # 端到端測試
├── index.html
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.ts
├── .env.example
├── .env.development
├── .env.production
└── package.json
```

### 2.2 Nuxt 3 專案結構（SSR / SSG）

```
project-root/
├── app.vue                       # 根組件
├── pages/                        # 基於文件的路由
│   ├── index.vue
│   ├── login.vue
│   └── dashboard/
│       └── index.vue
├── components/                   # 自動導入組件
├── composables/                  # 自動導入組合式函數
├── stores/                       # Pinia stores
├── server/                       # 伺服器端 API
│   ├── api/
│   └── middleware/
├── layouts/                      # 佈局模板
│   ├── default.vue
│   └── admin.vue
├── middleware/                    # 路由中間件
├── plugins/                      # Nuxt 插件
├── utils/                        # 工具函數（自動導入）
├── types/
├── public/
├── assets/
├── nuxt.config.ts
└── package.json
```

---

## 三、Vue 代碼規範

### 3.1 命名規範

```typescript
// 組件名：PascalCase（多詞，避免與 HTML 元素衝突）
// ✅ UserProfile.vue, AppButton.vue
// ❌ Button.vue, header.vue

// 組合式函數：use 前綴 + camelCase
// useAuth.ts, usePagination.ts

// Store：use 前綴 + 名詞 + Store
// useUserStore, useAppStore

// 事件名：kebab-case
// emit('update-profile'), emit('item-click')

// Props：camelCase（模板中自動轉 kebab-case）
defineProps<{
  userName: string
  isActive: boolean
}>()

// 路由名：kebab-case
{ name: 'user-profile', path: '/user/:id' }

// API 函數：動詞 + 名詞
// getUsers(), createOrder(), deleteItem()

// 常量：UPPER_SNAKE_CASE
const MAX_PAGE_SIZE = 50
```

### 3.2 組件規範

```vue
<!-- 使用 <script setup> + TypeScript -->
<script setup lang="ts">
// 1. 導入
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import type { User } from '@/types/user'

// 2. Props & Emits
const props = defineProps<{
  userId: number
  showAvatar?: boolean
}>()

const emit = defineEmits<{
  'update': [user: User]
  'delete': [id: number]
}>()

// 3. Store / Composables
const userStore = useUserStore()

// 4. 響應式數據
const loading = ref(false)
const user = ref<User | null>(null)

// 5. 計算屬性
const displayName = computed(() => user.value?.name ?? '未知用戶')

// 6. 方法
async function fetchUser() {
  loading.value = true
  try {
    user.value = await userStore.getUser(props.userId)
  } finally {
    loading.value = false
  }
}

// 7. 生命周期
onMounted(() => {
  fetchUser()
})
</script>

<template>
  <!-- 模板保持簡潔，複雜邏輯放到 computed 或方法中 -->
</template>

<style scoped>
/* 使用 scoped 避免樣式污染 */
</style>
```

### 3.3 必須遵守的規則

- **必須**使用 Composition API（`<script setup>`），禁止在新代碼中使用 Options API
- **必須**使用 TypeScript，所有 Props、Emits、API 返回值需有類型定義
- 組件模板中**禁止**編寫複雜邏輯（超過一行的表達式必須抽到 computed 或 method）
- **禁止**直接操作 DOM（使用 `ref` / `template ref` 替代 `document.querySelector`）
- **禁止**在組件中直接調用 API，必須通過 `api/` 層或 `store` 層
- 列表渲染**必須**提供唯一的 `:key`，禁止使用 index 作為 key（除非列表不變）
- 使用 `v-show` 處理頻繁切換，`v-if` 處理條件渲染
- 大型表單使用 VeeValidate 或自定義 composable 管理

---

## 四、API 請求層規範

### 4.1 Axios 封裝

```typescript
// api/index.ts
import axios from 'axios'
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import { useUserStore } from '@/stores/user'
import router from '@/router'

const request: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 15000,
})

// 請求攔截器
request.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const userStore = useUserStore()
  if (userStore.token) {
    config.headers.Authorization = `Bearer ${userStore.token}`
  }
  return config
})

// 響應攔截器
request.interceptors.response.use(
  (response: AxiosResponse) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      const userStore = useUserStore()
      userStore.logout()
      router.push({ name: 'login' })
    }
    return Promise.reject(error)
  }
)

export default request
```

### 4.2 API 模塊範例

```typescript
// api/user.ts
import request from './index'
import type { ApiResponse, PaginatedData } from '@/types/api'
import type { User, UserCreate, UserUpdate } from '@/types/user'

export function getUsers(params: { page: number; per_page: number }) {
  return request.get<any, ApiResponse<PaginatedData<User>>>('/users', { params })
}

export function getUserById(id: number) {
  return request.get<any, ApiResponse<User>>(`/users/${id}`)
}

export function createUser(data: UserCreate) {
  return request.post<any, ApiResponse<User>>('/users', data)
}

export function updateUser(id: number, data: UserUpdate) {
  return request.put<any, ApiResponse<User>>(`/users/${id}`, data)
}

export function deleteUser(id: number) {
  return request.delete<any, ApiResponse<null>>(`/users/${id}`)
}
```

---

## 五、狀態管理規範（Pinia）

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getUserInfo, login as loginApi } from '@/api/auth'
import type { User, LoginParams } from '@/types/user'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref<string>(localStorage.getItem('token') ?? '')
  const user = ref<User | null>(null)

  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const userName = computed(() => user.value?.name ?? '')

  // Actions
  async function login(params: LoginParams) {
    const res = await loginApi(params)
    token.value = res.data.token
    localStorage.setItem('token', res.data.token)
    await fetchUserInfo()
  }

  async function fetchUserInfo() {
    const res = await getUserInfo()
    user.value = res.data
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  return { token, user, isLoggedIn, userName, login, fetchUserInfo, logout }
})
```

---

## 六、路由與權限

### 6.1 路由守衛

```typescript
// router/guards.ts
import type { Router } from 'vue-router'
import { useUserStore } from '@/stores/user'

const whiteList = ['/login', '/register', '/404']

export function setupRouterGuards(router: Router) {
  router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore()

    if (whiteList.includes(to.path)) {
      return next()
    }

    if (!userStore.isLoggedIn) {
      return next({ path: '/login', query: { redirect: to.fullPath } })
    }

    // 檢查路由所需權限
    if (to.meta.permissions) {
      const required = to.meta.permissions as string[]
      const hasPermission = required.some(p => userStore.user?.permissions.includes(p))
      if (!hasPermission) {
        return next('/403')
      }
    }

    next()
  })
}
```

### 6.2 路由 Meta 類型

```typescript
// types/router.d.ts
import 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    permissions?: string[]
    requiresAuth?: boolean
    layout?: 'default' | 'admin' | 'blank'
  }
}
```

---

## 七、三端響應式設計

### 7.1 斷點定義

| 端 | 斷點範圍 | 佈局策略 |
|----|----------|----------|
| 手機端 | < 768px | 單列、底部導航、漢堡選單、觸控友善（44px 最小點擊區域） |
| 平板端 | 768px - 1024px | 雙列、側邊欄可收合 |
| 桌面端 | > 1024px | 多列、固定側邊欄 |

### 7.2 響應式 Composable

```typescript
// composables/useBreakpoint.ts
import { ref, onMounted, onUnmounted } from 'vue'

type Breakpoint = 'mobile' | 'tablet' | 'desktop'

export function useBreakpoint() {
  const breakpoint = ref<Breakpoint>('desktop')

  function update() {
    const width = window.innerWidth
    if (width < 768) breakpoint.value = 'mobile'
    else if (width < 1024) breakpoint.value = 'tablet'
    else breakpoint.value = 'desktop'
  }

  onMounted(() => {
    update()
    window.addEventListener('resize', update)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', update)
  })

  return { breakpoint }
}
```

---

## 八、環境變數規範

```env
# .env.development
VITE_API_BASE_URL=http://localhost:8080/api/v1
VITE_APP_TITLE=MyApp (Dev)

# .env.production
VITE_API_BASE_URL=https://api.example.com/api/v1
VITE_APP_TITLE=MyApp
```

- 所有前端環境變數必須以 `VITE_` 前綴
- **禁止**在前端代碼中存放 API Secret 或私鑰
- 使用 `import.meta.env.VITE_XXX` 訪問

---

## 九、安全規範

- 所有用戶輸入必須做 XSS 過濾（Vue 模板默認轉義，但 `v-html` 需手動處理）
- **禁止**使用 `v-html` 渲染不可信內容
- Token 存儲優先使用 `httpOnly cookie`，退而求其次使用 `localStorage`
- 敏感路由（如後台）必須配置路由守衛
- 所有 API 請求帶上 CSRF token（如後端要求）
- 第三方依賴定期更新，使用 `npm audit` 檢查漏洞

---

## 十、測試規範

```typescript
// tests/unit/components/UserCard.test.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import UserCard from '@/components/business/UserCard.vue'

describe('UserCard', () => {
  it('renders user name', () => {
    const wrapper = mount(UserCard, {
      props: { userName: 'Alice', isActive: true }
    })
    expect(wrapper.text()).toContain('Alice')
  })

  it('emits delete event on button click', async () => {
    const wrapper = mount(UserCard, {
      props: { userName: 'Alice', userId: 1 }
    })
    await wrapper.find('[data-testid="delete-btn"]').trigger('click')
    expect(wrapper.emitted('delete')).toBeTruthy()
  })
})
```

---

## 十一、專案指令

| 命令 | 行為 |
|------|------|
| `/init-vue` | 生成 Vue 3 + TypeScript + Vite 專案骨架（含完整目錄結構、路由、Store、API 層） |
| `/init-nuxt` | 生成 Nuxt 3 專案骨架 |
| `/init-auth` | 生成前端認證系統（登入、註冊、Token 管理、路由守衛） |
| `/init-admin` | 生成後台管理佈局框架（側邊欄、頂部導航、麵包屑、權限選單） |
| `/make-page <name>` | 生成頁面組件 + 路由配置 + API 模塊 |
| `/make-crud <model>` | 生成完整 CRUD 頁面（列表、表單、詳情） + API + Store |
| `/make-component <name>` | 生成組件模板（含 Props、Emits、測試文件） |
| `/check-types` | 執行 `vue-tsc --noEmit` 類型檢查 |
| `/check-lint` | 執行 ESLint + Stylelint 檢查 |
