# Backend Toolkit

一個基於 Django REST Framework 的後端工具包，整合了 Mock Data 生成器、開發輔助工具與標準化的架構。

## 🚀 快速啟動

### 使用 Docker (推薦)
1. 複製環境變數範本：
   ```bash
   cp .env.example .env
   ```
2. 啟動服務：
   ```bash
   docker-compose up -d
   ```
3. 執行資料庫遷移：
   ```bash
   docker-compose exec web python manage.py migrate
   ```

### 本地開發環境
1. 建立虛擬環境：
   ```bash
   python -m venv .venv
   ```
2. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```

## 📁 專案架構
- `config/`: 專案核心設定 (Settings, URLs, WSGI/ASGI)
- `apps/`: 功能模組存放地
- `utils/`: 共用工具函數
- `scripts/`: 管理與初始化腳本
- `static/` & `media/`: 靜態與媒體檔案

## 🛠 技術棧
- Python 3.13
- Django 5.2 LTS
- Django REST Framework
- PostgreSQL 15
- Redis 7
- Docker
