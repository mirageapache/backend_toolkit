# 🦄 Backend Toolkit - Mock Data 引擎

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一個強大且靈活的假資料生成引擎，基於 Django REST Framework 開發。支援預設模板（使用者、文章、產品、評論）以及強大的「自定義 Schema」功能，讓開發者能即時產出符合任何業務邏輯的 Mock Data。

---

## ✨ 核心特性

- 🚀 **預設生成器**：一鍵產生 User, Post, Product, Comment 的假資料。
- 🪄 **自定義 Schema**：透過簡單的 JSON 規則（支援全部 Faker 方法），定義專屬的資料結構。
- ⚡ **Redis 高速快取**：自動快取生成結果，大幅提升重複請求的響應速度。
- 📖 **互動式文件**：整合 `drf-spectacular` 自動生成 Swagger UI，即時測試 API。
- 🛡️ **安全驗證**：嚴格檢查自定義 Schema 語法，防止無效輸入。
- 🐳 **Docker 環境**：提供開發與正式環境兩套配置，無縫接軌部署。

---

## 🛠 技術棧

- **核心框架**: Django 5.2 LTS, Django REST Framework
- **資料庫**: PostgreSQL 15 (主儲存), Redis 7 (快取)
- **資料生成**: Faker Library
- **文件引擎**: drf-spectacular (OpenAPI 3.0)
- **部署工具**: Docker, Nginx, Gunicorn
- **品質控管**: Black, Flake8, isort

---

## 🚀 快速啟動

### 1. 環境準備
複製環境變數範本並設定：
```bash
cp .env.example .env
```

### 2. 開發環境 (Development)
適合日常開發，支援 **Auto-reload**。
```bash
# 啟動服務 (對外埠號: 8000)
docker compose -f docker-compose-dev.yml up -d --build

# 執行資料庫遷移
docker compose -f docker-compose-dev.yml exec web python manage.py migrate
```
存取路徑：`http://localhost:8000/api/mock/`

### 3. 正式環境 (Production)
使用 **Gunicorn + Nginx** 反向代理架構。
```bash
# 啟動服務 (對外埠號: 80)
docker compose up -d --build

# 收集靜態檔案 (若有更新 CSS/JS)
docker compose exec web python manage.py collectstatic --noinput
```
存取路徑：`http://localhost/api/mock/`

---

## 📖 API 文件與測試

啟動服務後，訪問以下路徑查看完整 API 說明：
- **Swagger UI**: `http://localhost/api/docs/` (正式) 或 `:8000/api/docs/` (開發)

### 常見端點範例：
- `GET /api/mock/users/?count=5`: 產生 5 筆使用者。
- `POST /api/mock/custom/`: 即時依據傳入的 JSON Schema 產生資料。

---

## 🧪 測試與代碼品質

### 執行自動化測試
```bash
docker compose exec web python manage.py test apps.mock_data
```

### 代碼品質檢查
```bash
# 排序 Import
docker compose exec web isort .
# 格式化代碼
docker compose exec web black .
# 語法與規範檢查
docker compose exec web flake8
```

---

## 📁 專案架構
- `apps/core/`: 存放共用的 BaseModel, Pagination, Exception Handler 等核心組件。
- `apps/mock_data/`: 包含 Generator 邏輯、ViewSet 與 Model 定義。
- `config/`: 專案全域設定。
- `nginx/`: Nginx 伺服器配置。

---

## 📄 License
本項目採用 MIT 授權。
