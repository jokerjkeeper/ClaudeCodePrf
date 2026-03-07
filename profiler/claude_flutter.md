# claude_flutter.md — Flutter 專案配置 Profile

> 本文件為 Flutter 專案的 Claude Code 補充規則，需搭配 `CLAUDE.md` 主文件使用。
> 放置於專案根目錄，與 CLAUDE.md 同級。

---

## 一、專案基礎資訊

```yaml
# ⚠️ 請根據實際專案填寫以下內容
framework: Flutter 3               # Flutter 3.x
language: Dart 3                   # Dart 3.x
state_management: Riverpod 2       # Riverpod / Bloc / GetX / Provider
navigation: GoRouter               # GoRouter / AutoRoute / Navigator 2.0
http_client: Dio                   # Dio / http / Chopper
local_storage: SharedPreferences   # SharedPreferences / Hive / Isar
database: Drift                    # Drift / sqflite / Isar / none
target_platforms:                  # 目標平台
  - Android
  - iOS
  - Web                            # 可選
  - macOS                          # 可選
min_android_sdk: 21                # Android 最低 SDK 版本
min_ios_version: "13.0"            # iOS 最低版本
```

---

## 二、專案結構

### 2.1 標準 Flutter 專案結構

```
project-root/
├── lib/
│   ├── main.dart                  # 應用入口
│   ├── app.dart                   # MaterialApp / App 配置
│   ├── router/                    # 路由配置
│   │   ├── app_router.dart
│   │   └── route_names.dart
│   ├── features/                  # 功能模塊（按業務領域劃分）
│   │   ├── auth/                  # 認證模塊
│   │   │   ├── data/
│   │   │   │   ├── models/        # 數據模型 / DTO
│   │   │   │   ├── repositories/  # Repository 實現
│   │   │   │   └── sources/       # 數據源（API / Local）
│   │   │   ├── domain/
│   │   │   │   ├── entities/      # 業務實體
│   │   │   │   └── repositories/  # Repository 接口
│   │   │   └── presentation/
│   │   │       ├── screens/       # 頁面
│   │   │       ├── widgets/       # 模塊內組件
│   │   │       └── providers/     # 狀態管理（Riverpod）
│   │   ├── home/
│   │   └── settings/
│   ├── core/                      # 核心通用模塊
│   │   ├── constants/             # 常量
│   │   │   ├── app_colors.dart
│   │   │   ├── app_sizes.dart
│   │   │   └── api_endpoints.dart
│   │   ├── network/               # 網絡層
│   │   │   ├── dio_client.dart
│   │   │   ├── api_interceptor.dart
│   │   │   └── api_exception.dart
│   │   ├── theme/                 # 主題
│   │   │   ├── app_theme.dart
│   │   │   └── text_styles.dart
│   │   ├── utils/                 # 工具函數
│   │   │   ├── formatters.dart
│   │   │   ├── validators.dart
│   │   │   └── extensions.dart
│   │   └── widgets/               # 通用可復用組件
│   │       ├── app_button.dart
│   │       ├── app_text_field.dart
│   │       └── loading_overlay.dart
│   └── l10n/                      # 國際化
│       ├── app_en.arb
│       └── app_zh.arb
├── test/                          # 測試
│   ├── unit/
│   ├── widget/
│   └── integration/
├── assets/                        # 資源文件
│   ├── images/
│   ├── icons/
│   └── fonts/
├── android/
├── ios/
├── web/                           # 如支持 Web
├── pubspec.yaml
├── analysis_options.yaml          # Lint 配置
├── .env.example
└── l10n.yaml
```

### 2.2 簡化結構（小型專案）

```
lib/
├── main.dart
├── app.dart
├── models/                        # 所有數據模型
├── services/                      # API 與業務邏輯
├── providers/                     # 狀態管理
├── screens/                       # 頁面
├── widgets/                       # 可復用組件
├── utils/                         # 工具函數
└── constants/                     # 常量
```

---

## 三、Dart 代碼規範

### 3.1 命名規範

```dart
// 類名：PascalCase
class UserProfile {}
class AuthRepository {}

// 文件名：snake_case
// user_profile.dart, auth_repository.dart

// 變數 / 函數 / 方法：camelCase
final userName = 'Alice';
void fetchUserData() {}

// 常量：camelCase（Dart 官方風格）
const maxLoginAttempts = 5;
const defaultPageSize = 20;

// 枚舉值：camelCase
enum UserRole { superAdmin, admin, member }

// 私有成員：_前綴
String _token = '';
void _handleError() {}

// Provider 命名（Riverpod）
final userProvider = StateNotifierProvider<UserNotifier, UserState>(...);
final authRepositoryProvider = Provider<AuthRepository>(...);
```

### 3.2 組件（Widget）規範

```dart
/// 使用者資料卡片
class UserCard extends StatelessWidget {
  const UserCard({
    super.key,
    required this.user,
    this.onTap,
  });

  final User user;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(user.name, style: Theme.of(context).textTheme.titleMedium),
              const SizedBox(height: 8),
              Text(user.email, style: Theme.of(context).textTheme.bodySmall),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 3.3 必須遵守的規則

- **必須**使用 `const` 構造函數（能 const 的地方全部加 const）
- **必須**為所有公開 API 添加文檔註釋（`///`）
- **禁止**在 Widget 的 `build` 方法中執行異步操作或副作用
- **禁止**在 build 中使用 `setState` 以外的方式觸發重建（應使用狀態管理方案）
- 優先使用 `StatelessWidget`，僅在需要局部狀態時使用 `StatefulWidget`
- 使用 `final` 優先於 `var`，使用 `const` 優先於 `final`
- Widget 拆分粒度：超過 80 行的 build 方法必須拆分為子 Widget 或私有方法
- 使用 `Theme.of(context)` 獲取顏色和文字樣式，禁止硬編碼顏色值
- 圖片資源使用 `flutter_gen` 或常量引用，禁止硬編碼路徑字串

---

## 四、網絡層規範

### 4.1 Dio 封裝

```dart
// core/network/dio_client.dart
class DioClient {
  late final Dio _dio;

  DioClient({required String baseUrl, String? token}) {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 15),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
    ));

    _dio.interceptors.addAll([
      LogInterceptor(requestBody: true, responseBody: true),
      AuthInterceptor(),
    ]);
  }

  Future<T> get<T>(String path, {Map<String, dynamic>? queryParameters}) async {
    final response = await _dio.get(path, queryParameters: queryParameters);
    return response.data as T;
  }

  Future<T> post<T>(String path, {dynamic data}) async {
    final response = await _dio.post(path, data: data);
    return response.data as T;
  }

  Future<T> put<T>(String path, {dynamic data}) async {
    final response = await _dio.put(path, data: data);
    return response.data as T;
  }

  Future<T> delete<T>(String path) async {
    final response = await _dio.delete(path);
    return response.data as T;
  }
}
```

### 4.2 統一 API 響應模型

```dart
// core/network/api_response.dart
class ApiResponse<T> {
  final int code;
  final String message;
  final T? data;

  const ApiResponse({required this.code, required this.message, this.data});

  factory ApiResponse.fromJson(
    Map<String, dynamic> json,
    T Function(dynamic)? fromData,
  ) {
    return ApiResponse(
      code: json['code'] as int,
      message: json['message'] as String,
      data: json['data'] != null && fromData != null
          ? fromData(json['data'])
          : null,
    );
  }

  bool get isSuccess => code == 200;
}
```

### 4.3 統一異常處理

```dart
// core/network/api_exception.dart
class ApiException implements Exception {
  final int? statusCode;
  final String message;

  const ApiException({this.statusCode, required this.message});

  factory ApiException.fromDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return const ApiException(message: '網絡連接超時');
      case DioExceptionType.badResponse:
        return ApiException(
          statusCode: error.response?.statusCode,
          message: error.response?.data?['message'] ?? '伺服器錯誤',
        );
      default:
        return const ApiException(message: '網絡異常');
    }
  }
}
```

---

## 五、狀態管理規範（Riverpod）

### 5.1 Provider 結構

```dart
// features/auth/presentation/providers/auth_provider.dart

// 狀態類
@freezed
class AuthState with _$AuthState {
  const factory AuthState.initial() = _Initial;
  const factory AuthState.loading() = _Loading;
  const factory AuthState.authenticated(User user) = _Authenticated;
  const factory AuthState.unauthenticated() = _Unauthenticated;
  const factory AuthState.error(String message) = _Error;
}

// Notifier
class AuthNotifier extends StateNotifier<AuthState> {
  final AuthRepository _repository;

  AuthNotifier(this._repository) : super(const AuthState.initial());

  Future<void> login(String email, String password) async {
    state = const AuthState.loading();
    try {
      final user = await _repository.login(email, password);
      state = AuthState.authenticated(user);
    } on ApiException catch (e) {
      state = AuthState.error(e.message);
    }
  }

  void logout() {
    _repository.clearToken();
    state = const AuthState.unauthenticated();
  }
}

// Provider 定義
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.watch(authRepositoryProvider));
});
```

### 5.2 Bloc 替代方案

```dart
// 若使用 Bloc，遵循以下結構
// features/auth/presentation/bloc/
//   ├── auth_bloc.dart
//   ├── auth_event.dart
//   └── auth_state.dart
```

---

## 六、路由規範（GoRouter）

```dart
// router/app_router.dart
final goRouter = GoRouter(
  initialLocation: '/',
  redirect: (context, state) {
    final isLoggedIn = /* 檢查登入狀態 */;
    final isAuthRoute = state.matchedLocation.startsWith('/auth');

    if (!isLoggedIn && !isAuthRoute) return '/auth/login';
    if (isLoggedIn && isAuthRoute) return '/';
    return null;
  },
  routes: [
    GoRoute(
      path: '/auth/login',
      name: RouteNames.login,
      builder: (context, state) => const LoginScreen(),
    ),
    ShellRoute(
      builder: (context, state, child) => MainShell(child: child),
      routes: [
        GoRoute(
          path: '/',
          name: RouteNames.home,
          builder: (context, state) => const HomeScreen(),
        ),
        GoRoute(
          path: '/profile/:userId',
          name: RouteNames.profile,
          builder: (context, state) {
            final userId = state.pathParameters['userId']!;
            return ProfileScreen(userId: userId);
          },
        ),
      ],
    ),
  ],
);

// router/route_names.dart
abstract class RouteNames {
  static const login = 'login';
  static const home = 'home';
  static const profile = 'profile';
}
```

---

## 七、主題與樣式規範

### 7.1 統一主題配置

```dart
// core/theme/app_theme.dart
class AppTheme {
  static ThemeData light() {
    return ThemeData(
      useMaterial3: true,
      colorSchemeSeed: AppColors.primary,
      brightness: Brightness.light,
      textTheme: _textTheme,
      inputDecorationTheme: _inputTheme,
      elevatedButtonTheme: _buttonTheme,
    );
  }

  static ThemeData dark() {
    return ThemeData(
      useMaterial3: true,
      colorSchemeSeed: AppColors.primary,
      brightness: Brightness.dark,
      textTheme: _textTheme,
    );
  }
}

// core/constants/app_colors.dart
abstract class AppColors {
  static const primary = Color(0xFF1A73E8);
  static const error = Color(0xFFDC3545);
  static const success = Color(0xFF28A745);
}

// core/constants/app_sizes.dart
abstract class AppSizes {
  static const double xs = 4;
  static const double sm = 8;
  static const double md = 16;
  static const double lg = 24;
  static const double xl = 32;

  // 最小觸控區域
  static const double minTapTarget = 44;
}
```

### 7.2 響應式設計

```dart
// core/utils/responsive.dart
class Responsive {
  static bool isMobile(BuildContext context) =>
      MediaQuery.sizeOf(context).width < 768;

  static bool isTablet(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    return width >= 768 && width < 1024;
  }

  static bool isDesktop(BuildContext context) =>
      MediaQuery.sizeOf(context).width >= 1024;

  /// 根據斷點返回不同佈局
  static T value<T>(
    BuildContext context, {
    required T mobile,
    T? tablet,
    T? desktop,
  }) {
    if (isDesktop(context)) return desktop ?? tablet ?? mobile;
    if (isTablet(context)) return tablet ?? mobile;
    return mobile;
  }
}
```

---

## 八、數據模型規範

### 8.1 使用 freezed + json_serializable

```dart
// features/auth/data/models/user_model.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_model.freezed.dart';
part 'user_model.g.dart';

@freezed
class UserModel with _$UserModel {
  const factory UserModel({
    required int id,
    required String name,
    required String email,
    @JsonKey(name: 'created_at') required DateTime createdAt,
    String? avatar,
  }) = _UserModel;

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);
}
```

### 8.2 模型層級規範

- `data/models/` — API 序列化/反序列化用的 DTO
- `domain/entities/` — 業務實體（不依賴序列化）
- 簡單專案可合併為一層

---

## 九、安全規範

- Token 存儲使用 `flutter_secure_storage`，禁止使用 `SharedPreferences` 存放敏感資料
- API Base URL 和密鑰通過 `--dart-define` 或 `.env` 注入，禁止硬編碼
- 所有用戶輸入必須驗證（使用 `Form` + `TextFormField` + `validator`）
- 啟用 ProGuard / R8（Android）和 Bitcode（iOS）混淆
- 網絡請求使用 HTTPS，啟用 Certificate Pinning（如需要）
- 禁止在日誌中輸出用戶敏感資料（密碼、Token）

---

## 十、測試規範

```dart
// test/unit/features/auth/auth_repository_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

@GenerateMocks([DioClient])
void main() {
  late AuthRepository repository;
  late MockDioClient mockDio;

  setUp(() {
    mockDio = MockDioClient();
    repository = AuthRepositoryImpl(mockDio);
  });

  group('login', () {
    test('should return user on successful login', () async {
      when(mockDio.post('/auth/login', data: anyNamed('data')))
          .thenAnswer((_) async => mockLoginResponse);

      final result = await repository.login('test@example.com', 'password');

      expect(result.email, 'test@example.com');
      verify(mockDio.post('/auth/login', data: anyNamed('data'))).called(1);
    });

    test('should throw ApiException on invalid credentials', () async {
      when(mockDio.post('/auth/login', data: anyNamed('data')))
          .thenThrow(DioException(requestOptions: RequestOptions()));

      expect(
        () => repository.login('test@example.com', 'wrong'),
        throwsA(isA<ApiException>()),
      );
    });
  });
}

// test/widget/features/auth/login_screen_test.dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('should show error on empty email submit', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: LoginScreen()));

    await tester.tap(find.byType(ElevatedButton));
    await tester.pump();

    expect(find.text('請輸入郵箱'), findsOneWidget);
  });
}
```

---

## 十一、常用套件推薦

| 類別 | 套件 | 用途 |
|------|------|------|
| 狀態管理 | `flutter_riverpod` / `flutter_bloc` | 狀態管理 |
| 路由 | `go_router` | 聲明式路由 |
| 網絡 | `dio` | HTTP 客戶端 |
| 序列化 | `freezed` + `json_serializable` | 不可變模型 + JSON 序列化 |
| 本地存儲 | `flutter_secure_storage` | 安全存儲 |
| 國際化 | `flutter_localizations` + `intl` | 多語言 |
| 圖片 | `cached_network_image` | 圖片緩存 |
| UI | `flutter_screenutil` | 螢幕適配 |
| 代碼生成 | `build_runner` | 生成 freezed / json 代碼 |
| Lint | `flutter_lints` / `very_good_analysis` | 靜態分析 |

---

## 十二、專案指令

| 命令 | 行為 |
|------|------|
| `/init-flutter` | 生成 Flutter 專案骨架（含完整目錄結構、路由、狀態管理、網絡層） |
| `/init-auth` | 生成認證系統（登入/註冊頁面、Token 管理、路由守衛） |
| `/make-feature <name>` | 生成功能模塊骨架（data / domain / presentation 三層） |
| `/make-screen <name>` | 生成頁面 + 路由配置 |
| `/make-model <name>` | 生成 freezed 數據模型（含 fromJson） |
| `/make-provider <name>` | 生成 Riverpod Provider + State（或 Bloc） |
| `/run-build` | 執行 `dart run build_runner build --delete-conflicting-outputs` |
| `/check-lint` | 執行 `dart analyze` 靜態分析 |
| `/check-test` | 執行 `flutter test` 全部測試 |
