# 測試文件 (TEST_README)

本文件整理專案中所有的測試指令與說明。

---

## 前置條件

執行任何測試前，請確保 Docker 容器正在運行：

```bash
docker compose up -d
```

確認容器狀態：

```bash
docker compose ps
```

---

## 一、單元測試

使用 Django 內建的測試框架，測試時會自動建立 **暫時的測試資料庫**，測試結束後自動銷毀，不影響開發資料庫。

### 執行全部測試

```bash
docker compose exec web python manage.py test
```

### 執行 Core App 全部測試

```bash
docker compose exec web python manage.py test apps.core.tests
```

### 執行特定測試檔案

```bash
# BaseModel 測試（UUID、時間戳記、排序）
docker compose exec web python manage.py test apps.core.tests.test_models

# 權限測試（IsAdminOrReadOnly）
docker compose exec web python manage.py test apps.core.tests.test_permissions

# 分頁測試（StandardResultSetPagination）
docker compose exec web python manage.py test apps.core.tests.test_pagination

# Mixin 測試（SoftDelete、Timestamp）
docker compose exec web python manage.py test apps.core.tests.test_mixins
```

### 執行單一測試方法

```bash
# 格式：<測試檔案路徑>.<TestCase 類別名稱>.<測試方法名稱>
docker compose exec web python manage.py test apps.core.tests.test_models.BaseModelTestCase.test_uuid_primary_key
```

### 顯示詳細測試結果

加上 `--verbosity=2` 參數可以看到每個測試方法的名稱與結果：

```bash
docker compose exec web python manage.py test apps.core.tests --verbosity=2
```

### 測試涵蓋範圍

| 測試檔案 | 測試數量 | 測試內容 |
|---|---|---|
| `test_models.py` | 5 | UUID 主鍵、`created_at`、`updated_at`、`is_active`、排序 |
| `test_permissions.py` | 3 | GET 公開、POST 一般用戶拒絕、POST 管理員允許 |
| `test_pagination.py` | 3 | 預設分頁大小、自訂大小、回應格式 |
| `test_mixins.py` | 2 | 軟刪除、真實刪除 |
| **合計** | **13** | |

---

## 二、環境驗證腳本

直接連接**開發資料庫**，驗證整個基礎設施是否正常運作。

```bash
docker compose exec web python scripts/verify_environment.py
```

### 驗證項目

| 檢查項目 | 驗證內容 |
|---|---|
| PostgreSQL | 連線成功並顯示版本 |
| Redis | 寫入、讀取、刪除快取 |
| Installed Apps | `core`、`rest_framework`、`corsheaders` 已安裝 |

### 預期輸出

```
==================================================
  Phase 1 環境驗證
==================================================

[PostgreSQL 資料庫檢查]
  ✓ 連線成功: PostgreSQL 15.15 on x86_64-pc-linux-musl

[Redis 快取檢查]
  ✓ 寫入並讀取成功

[已安裝 Apps 檢查]
  ✓ 已安裝: core
  ✓ 已安裝: rest_framework
  ✓ 已安裝: corsheaders

[驗證總結]
  ✓ 通過: PostgreSQL
  ✓ 通過: Redis
  ✓ 通過: Installed Apps

總計: 3/3 項通過

🎉 Phase 1 環境配置完成！
```

---

## 三、系統設定檢查

Django 內建的設定檢查，確認設定檔與 App 的語法是否正確：

```bash
docker compose exec web python manage.py check
```

預期輸出：`System check identified no issues (0 silenced).`

---

## 四、常見問題排除

### `service "web" is not running`
Docker 容器尚未啟動，請執行：
```bash
docker compose up -d
```

### `ModuleNotFoundError: No module named 'django'`
你在本機（非 Docker）執行了 `python` 指令，請改用 `docker compose exec web python`。

### 測試數量少於預期（如只有 2 個而非 5 個）
可能是**縮排錯誤**，測試方法沒有正確縮排到 `TestCase` 類別內，導致 Django 找不到它們。
