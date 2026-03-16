from .base import *

DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "web"]

# 靜態檔案路徑 (供 Nginx 使用)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# 安全性設定 (本地測試暫時關閉 SSL 強制導向)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

